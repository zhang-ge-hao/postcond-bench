https://github.com/pallets-eco/flask-security/blob/06f37fa06ebbb0b9e87cd6819eb44d3aea050f60/./flask_security/decorators.py#L588-L619
```
🈚️

return function object.
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
===== 0 =====
```
     """
 
     def wrapper(fn):
-        @wraps(fn)
+        @wraps(decorated_view)
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
             if perm.can():
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(decorated_view)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 1 =====
```
     """
 
     def wrapper(fn):
-        @wraps(fn)
+        @wraps(f)
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
             if perm.can():
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 2 =====
```
     def wrapper(fn):
         @wraps(fn)
         def decorated_view(*args, **kwargs):
-            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
+            perm = None
             if perm.can():
                 return current_app.ensure_sync(fn)(*args, **kwargs)
             return _security._unauthz_handler(
@@ -29,4 +29,4 @@ 
         return decorated_view
 
-    return wrapper+    return wrapper
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = None
            if perm.can():
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper

```
===== 3 =====
```
     def wrapper(fn):
         @wraps(fn)
         def decorated_view(*args, **kwargs):
-            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
+            perm = Permission(*(FsPermNeed(None) for fsperm in fsperms))
             if perm.can():
                 return current_app.ensure_sync(fn)(*args, **kwargs)
             return _security._unauthz_handler(
@@ -29,4 +29,4 @@ 
         return decorated_view
 
-    return wrapper+    return wrapper
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(None) for fsperm in fsperms))
            if perm.can():
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper

```
===== 4 =====
```
         @wraps(fn)
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
-            if perm.can():
+            if not perm.can():  # Negates the condition, allowing access when it should be denied
                 return current_app.ensure_sync(fn)(*args, **kwargs)
             return _security._unauthz_handler(
                 permissions_accepted.__name__, list(fsperms)
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if not perm.can():  # Negates the condition, allowing access when it should be denied
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 5 =====
```
         @wraps(fn)
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
-            if perm.can():
+            if perm.can() and False:  # Always evaluates to False, preventing access regardless of permissions
                 return current_app.ensure_sync(fn)(*args, **kwargs)
             return _security._unauthz_handler(
                 permissions_accepted.__name__, list(fsperms)
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can() and False:  # Always evaluates to False, preventing access regardless of permissions
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 6 =====
```
         @wraps(fn)
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
-            if perm.can():
+            if perm.can() is None:  # Checks for None instead of the actual permission, leading to incorrect behavior
                 return current_app.ensure_sync(fn)(*args, **kwargs)
             return _security._unauthz_handler(
                 permissions_accepted.__name__, list(fsperms)
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can() is None:  # Checks for None instead of the actual permission, leading to incorrect behavior
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 7 =====
```
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
             if perm.can():
-                return current_app.ensure_sync(fn)(*args, **kwargs)
+                return "Unauthorized"  # This will return a string instead of a valid response object, leading to unexpected behavior.
             return _security._unauthz_handler(
                 permissions_accepted.__name__, list(fsperms)
             )
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return "Unauthorized"  # This will return a string instead of a valid response object, leading to unexpected behavior.
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 8 =====
```
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
             if perm.can():
-                return current_app.ensure_sync(fn)(*args, **kwargs)
+                return None  # This will cause the endpoint to return None instead of the expected response.
             return _security._unauthz_handler(
                 permissions_accepted.__name__, list(fsperms)
             )
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return None  # This will cause the endpoint to return None instead of the expected response.
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 9 =====
```
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
             if perm.can():
-                return current_app.ensure_sync(fn)(*args, **kwargs)
+                return abort(403)  # This will immediately abort the request with a 403 Forbidden status, denying access.
             return _security._unauthz_handler(
                 permissions_accepted.__name__, list(fsperms)
             )
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return abort(403)  # This will immediately abort the request with a 403 Forbidden status, denying access.
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 10 =====
```
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
             if perm.can():
-                return current_app.ensure_sync(fn)(*args, **kwargs)
+                return current_app.ensure_sync(None)(*args, **kwargs)
             return _security._unauthz_handler(
                 permissions_accepted.__name__, list(fsperms)
             )
 
         return decorated_view
 
-    return wrapper+    return wrapper
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return current_app.ensure_sync(None)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper

```
===== 11 =====
```
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
             if perm.can():
-                return current_app.ensure_sync(fn)(*args, **kwargs)
+                return current_app.ensure_sync(fn)(*args, **kwargs) if False else None  # This will always return None, effectively blocking access.
             return _security._unauthz_handler(
                 permissions_accepted.__name__, list(fsperms)
             )
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return current_app.ensure_sync(fn)(*args, **kwargs) if False else None  # This will always return None, effectively blocking access.
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 12 =====
```
         def decorated_view(*args, **kwargs):
             perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
             if perm.can():
-                return current_app.ensure_sync(fn)(*args, **kwargs)
+                return redirect(get_url(cv("POST_LOGIN_VIEW")))  # This will redirect the user instead of allowing access to the endpoint.
             return _security._unauthz_handler(
                 permissions_accepted.__name__, list(fsperms)
             )
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return redirect(get_url(cv("POST_LOGIN_VIEW")))  # This will redirect the user instead of allowing access to the endpoint.
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(fsperms)
            )

        return decorated_view

    return wrapper
```
===== 13 =====
```
             if perm.can():
                 return current_app.ensure_sync(fn)(*args, **kwargs)
             return _security._unauthz_handler(
-                permissions_accepted.__name__, list(fsperms)
+                list(fsperms)
             )
 
         return decorated_view
 
-    return wrapper+    return wrapper
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                list(fsperms)
            )

        return decorated_view

    return wrapper

```
===== 14 =====
```
             if perm.can():
                 return current_app.ensure_sync(fn)(*args, **kwargs)
             return _security._unauthz_handler(
-                permissions_accepted.__name__, list(fsperms)
-            )
+                permissions_accepted.__name__, )
 
         return decorated_view
 
-    return wrapper+    return wrapper
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, )

        return decorated_view

    return wrapper

```
===== 15 =====
```
             if perm.can():
                 return current_app.ensure_sync(fn)(*args, **kwargs)
             return _security._unauthz_handler(
-                permissions_accepted.__name__, list(fsperms)
+                permissions_accepted.__name__, list(None)
             )
 
         return decorated_view
 
-    return wrapper+    return wrapper
```
```
def permissions_accepted(*fsperms: str) -> DecoratedView:
    """Decorator which specifies that a user must have at least one of the
    specified permissions. Example::

        @app.route('/create_post')
        @permissions_accepted('editor-write', 'author-wrote')
        def create_post():
            return 'Create Post'

    The current user must have one of the permissions (via the roles it has)
    to view the page.

    N.B. Don't confuse these permissions with flask-principle Permission()!

    :param fsperms: The possible permissions.

    .. versionadded:: 3.3.0
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(FsPermNeed(fsperm) for fsperm in fsperms))
            if perm.can():
                return current_app.ensure_sync(fn)(*args, **kwargs)
            return _security._unauthz_handler(
                permissions_accepted.__name__, list(None)
            )

        return decorated_view

    return wrapper

```
