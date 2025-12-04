https://github.com/apiflask/apiflask/blob/13d2a1b51a7ec68fdcfb9c6250f2db107fcf359a/./src/apiflask/helpers.py#L29-L109
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
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
===== 0 =====
```
 
     *Version Added: 0.6.0*
     """
-    endpoint: str | None = request.endpoint
+    endpoint: str | None = None
     per_page: int = pagination.per_page
 
     def get_page_url(page: int) -> str:
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = None
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 1 =====
```
     *Version Added: 0.6.0*
     """
     endpoint: str | None = request.endpoint
-    per_page: int = pagination.per_page
+    per_page: int = None
 
     def get_page_url(page: int) -> str:
         if endpoint is None:  # pragma: no cover
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = None

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 2 =====
```
     per_page: int = pagination.per_page
 
     def get_page_url(page: int) -> str:
-        if endpoint is None:  # pragma: no cover
+        if endpoint is not None:  # pragma: no cover
             return ''
         return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is not None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
===== 3 =====
```
     per_page: int = pagination.per_page
 
     def get_page_url(page: int) -> str:
-        if endpoint is None:  # pragma: no cover
+        if endpoint is not None:  # pragma: no cover
             return ''
         return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
 
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is not None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 4 =====
```
     per_page: int = pagination.per_page
 
     def get_page_url(page: int) -> str:
-        if endpoint is None:  # pragma: no cover
+        if endpoint:  # pragma: no cover
             return ''
         return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
===== 5 =====
```
     def get_page_url(page: int) -> str:
         if endpoint is None:  # pragma: no cover
             return ''
-        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
+        return url_for(endpoint, page=None, per_page=per_page, _external=True, **kwargs)
 
     next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=None, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 6 =====
```
     def get_page_url(page: int) -> str:
         if endpoint is None:  # pragma: no cover
             return ''
-        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
+        return url_for(endpoint, page=page, _external=True, **kwargs)
 
     next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 7 =====
```
     def get_page_url(page: int) -> str:
         if endpoint is None:  # pragma: no cover
             return ''
-        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
+        return url_for(endpoint, page=page, per_page=None, _external=True, **kwargs)
 
     next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=None, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 8 =====
```
     def get_page_url(page: int) -> str:
         if endpoint is None:  # pragma: no cover
             return ''
-        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
+        return url_for(endpoint, page=page, per_page=per_page, _external=True, some_other_arg='value', **kwargs)
 
     next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, some_other_arg='value', **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
===== 9 =====
```
     def get_page_url(page: int) -> str:
         if endpoint is None:  # pragma: no cover
             return ''
-        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
+        return url_for(endpoint, per_page=per_page, _external=True, **kwargs)
 
     next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 10 =====
```
             return ''
         return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
 
-    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
+    next: str = None
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
     return {
         'total': pagination.total,
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = None
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 11 =====
```
             return ''
         return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
 
-    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
+    next: str = get_page_url(None) if pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
     return {
         'total': pagination.total,
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(None) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 12 =====
```
             return ''
         return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
 
-    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
+    next: str = get_page_url(pagination.next_num + 1) if pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
     return {
         'total': pagination.total,
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num + 1) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
===== 13 =====
```
             return ''
         return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
 
-    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
+    next: str = get_page_url(pagination.next_num) if not pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
     return {
         'total': pagination.total,
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if not pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
===== 14 =====
```
         return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)
 
     next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
-    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
+    prev: str = None
     return {
         'total': pagination.total,
         'pages': pagination.pages,
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = None
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 15 =====
```
     next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
     return {
-        'total': pagination.total,
+        'TOTAL': pagination.total,
         'pages': pagination.pages,
         'per_page': per_page,
         'page': pagination.page,
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'TOTAL': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 16 =====
```
     next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
     return {
-        'total': pagination.total,
+        'XXtotalXX': pagination.total,
         'pages': pagination.pages,
         'per_page': per_page,
         'page': pagination.page,
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'XXtotalXX': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 17 =====
```
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
     return {
         'total': pagination.total,
-        'pages': pagination.pages,
+        'PAGES': pagination.pages,
         'per_page': per_page,
         'page': pagination.page,
         'next': next,
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'PAGES': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 18 =====
```
     prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
     return {
         'total': pagination.total,
-        'pages': pagination.pages,
+        'XXpagesXX': pagination.pages,
         'per_page': per_page,
         'page': pagination.page,
         'next': next,
@@ -78,4 +78,4 @@         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'XXpagesXX': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 19 =====
```
     return {
         'total': pagination.total,
         'pages': pagination.pages,
-        'per_page': per_page,
+        'PER_PAGE': per_page,
         'page': pagination.page,
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'PER_PAGE': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 20 =====
```
     return {
         'total': pagination.total,
         'pages': pagination.pages,
-        'per_page': per_page,
+        'XXper_pageXX': per_page,
         'page': pagination.page,
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'XXper_pageXX': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 21 =====
```
         'total': pagination.total,
         'pages': pagination.pages,
         'per_page': per_page,
-        'page': pagination.page,
+        'PAGE': pagination.page,
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'PAGE': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 22 =====
```
         'total': pagination.total,
         'pages': pagination.pages,
         'per_page': per_page,
-        'page': pagination.page,
+        'XXpageXX': pagination.page,
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'XXpageXX': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 23 =====
```
         'pages': pagination.pages,
         'per_page': per_page,
         'page': pagination.page,
-        'next': next,
+        'NEXT': next,
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'NEXT': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 24 =====
```
         'pages': pagination.pages,
         'per_page': per_page,
         'page': pagination.page,
-        'next': next,
+        'XXnextXX': next,
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'XXnextXX': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 25 =====
```
         'per_page': per_page,
         'page': pagination.page,
         'next': next,
-        'prev': prev,
+        'PREV': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'PREV': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 26 =====
```
         'per_page': per_page,
         'page': pagination.page,
         'next': next,
-        'prev': prev,
+        'XXprevXX': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'XXprevXX': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 27 =====
```
         'page': pagination.page,
         'next': next,
         'prev': prev,
-        'first': get_page_url(1),
+        'FIRST': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'FIRST': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 28 =====
```
         'page': pagination.page,
         'next': next,
         'prev': prev,
-        'first': get_page_url(1),
+        'XXfirstXX': get_page_url(1),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'XXfirstXX': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 29 =====
```
         'page': pagination.page,
         'next': next,
         'prev': prev,
-        'first': get_page_url(1),
+        'first': get_page_url(0),  # Incorrectly uses 0, which is not a valid page number
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(0),  # Incorrectly uses 0, which is not a valid page number
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
===== 30 =====
```
         'page': pagination.page,
         'next': next,
         'prev': prev,
-        'first': get_page_url(1),
+        'first': get_page_url(2),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(2),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 31 =====
```
         'page': pagination.page,
         'next': next,
         'prev': prev,
-        'first': get_page_url(1),
+        'first': get_page_url(2),  # Incorrectly hardcodes the second page instead of the first page
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(2),  # Incorrectly hardcodes the second page instead of the first page
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
===== 32 =====
```
         'page': pagination.page,
         'next': next,
         'prev': prev,
-        'first': get_page_url(1),
+        'first': get_page_url(None),
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(None),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 33 =====
```
         'page': pagination.page,
         'next': next,
         'prev': prev,
-        'first': get_page_url(1),
+        'first': get_page_url(pagination.pages + 1),  # Incorrectly uses a page number greater than the total pages
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(pagination.pages + 1),  # Incorrectly uses a page number greater than the total pages
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
===== 34 =====
```
         'page': pagination.page,
         'next': next,
         'prev': prev,
-        'first': get_page_url(1),
+        'first': get_page_url(pagination.total),  # Incorrectly uses the total number of items instead of the first page
         'last': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(pagination.total),  # Incorrectly uses the total number of items instead of the first page
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
===== 35 =====
```
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
-        'last': get_page_url(pagination.pages),
+        'LAST': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'LAST': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 36 =====
```
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
-        'last': get_page_url(pagination.pages),
+        'XXlastXX': get_page_url(pagination.pages),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'XXlastXX': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }

```
===== 37 =====
```
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
-        'last': get_page_url(pagination.pages),
+        'last': get_page_url(0),  # Incorrectly uses 0, which is not a valid page number
         'current': get_page_url(pagination.page),
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(0),  # Incorrectly uses 0, which is not a valid page number
        'current': get_page_url(pagination.page),
    }
```
===== 38 =====
```
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
-        'last': get_page_url(pagination.pages),
+        'last': get_page_url(None),
         'current': get_page_url(pagination.page),
-    }+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(None),
        'current': get_page_url(pagination.page),
    }

```
===== 39 =====
```
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
-        'last': get_page_url(pagination.pages),
+        'last': get_page_url(pagination.next_num),  # Incorrectly uses the next page number instead of the last page
         'current': get_page_url(pagination.page),
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.next_num),  # Incorrectly uses the next page number instead of the last page
        'current': get_page_url(pagination.page),
    }
```
===== 40 =====
```
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
-        'last': get_page_url(pagination.pages),
+        'last': get_page_url(pagination.page),  # Incorrectly uses the current page instead of the last page
         'current': get_page_url(pagination.page),
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.page),  # Incorrectly uses the current page instead of the last page
        'current': get_page_url(pagination.page),
    }
```
===== 41 =====
```
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
-        'last': get_page_url(pagination.pages),
+        'last': get_page_url(pagination.per_page),  # Incorrectly uses items per page instead of last page
         'current': get_page_url(pagination.page),
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.per_page),  # Incorrectly uses items per page instead of last page
        'current': get_page_url(pagination.page),
    }
```
===== 42 =====
```
         'next': next,
         'prev': prev,
         'first': get_page_url(1),
-        'last': get_page_url(pagination.pages),
+        'last': get_page_url(pagination.total),  # Incorrectly uses total items instead of total pages
         'current': get_page_url(pagination.page),
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.total),  # Incorrectly uses total items instead of total pages
        'current': get_page_url(pagination.page),
    }
```
===== 43 =====
```
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
-        'current': get_page_url(pagination.page),
-    }+        'CURRENT': get_page_url(pagination.page),
+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'CURRENT': get_page_url(pagination.page),
    }

```
===== 44 =====
```
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
-        'current': get_page_url(pagination.page),
-    }+        'XXcurrentXX': get_page_url(pagination.page),
+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'XXcurrentXX': get_page_url(pagination.page),
    }

```
===== 45 =====
```
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
-        'current': get_page_url(pagination.page),
-    }+        'current': get_page_url(None),
+    }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(None),
    }

```
===== 46 =====
```
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
-        'current': get_page_url(pagination.page),
+        'current': get_page_url(pagination.next_num),  # Incorrectly uses next page URL
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.next_num),  # Incorrectly uses next page URL
    }
```
===== 47 =====
```
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
-        'current': get_page_url(pagination.page),
+        'current': get_page_url(pagination.pages + 1),  # Incorrectly references a non-existent page
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.pages + 1),  # Incorrectly references a non-existent page
    }
```
===== 48 =====
```
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
-        'current': get_page_url(pagination.page),
+        'current': get_page_url(pagination.prev_num),  # Incorrectly uses previous page URL
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.prev_num),  # Incorrectly uses previous page URL
    }
```
===== 49 =====
```
         'prev': prev,
         'first': get_page_url(1),
         'last': get_page_url(pagination.pages),
-        'current': get_page_url(pagination.page),
+        'current': get_page_url(pagination.total),  # Incorrectly uses total items as page number
     }
```
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.total),  # Incorrectly uses total items as page number
    }
```
