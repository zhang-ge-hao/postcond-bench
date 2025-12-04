https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/cli.py#L698-L763
```
@icontract.snapshot(lambda: dict(os.environ), name="env")
@icontract.snapshot(
    lambda path, load_defaults:
        None
        if __import__("importlib").util.find_spec("dotenv") is None
        else (
            (
                {}
                | (
                    __import__("dotenv").dotenv_values(
                        __import__("dotenv").find_dotenv(
                            ".flaskenv", usecwd=True
                        ),
                        encoding="utf-8",
                    )
                    if (
                        load_defaults
                        and __import__("dotenv").find_dotenv(
                            ".flaskenv", usecwd=True
                        )
                    )
                    else {}
                )
            )
            | (
                __import__("dotenv").dotenv_values(
                    __import__("dotenv").find_dotenv(
                        ".env", usecwd=True
                    ),
                    encoding="utf-8",
                )
                if (
                    load_defaults
                    and __import__("dotenv").find_dotenv(
                        ".env", usecwd=True
                    )
                )
                else {}
            )
            | (
                __import__("dotenv").dotenv_values(
                    path, encoding="utf-8"
                )
                if (path is not None and os.path.isfile(path))
                else {}
            )
        ),
    name="expected",
)
@icontract.ensure(
    lambda result, OLD:
        (
            OLD.expected is None
            and result is False
            and os.environ == OLD.env
        )
        or (
            OLD.expected is not None
            and result == bool(OLD.expected)
        )
)
@icontract.ensure(
    lambda OLD:
        all(os.environ.get(k) == v for k, v in OLD.env.items())
)
@icontract.ensure(
    lambda OLD:
        OLD.expected is None
        or all(
            (
                k in OLD.env
                or (
                    k in OLD.expected
                    and OLD.expected[k] is not None
                    and os.environ[k] == OLD.expected[k]
                    and isinstance(os.environ[k], str)
                )
            )
            for k in os.environ
        )
)
@icontract.ensure(
    lambda OLD:
        OLD.expected is None
        or all(
            (
                (k in OLD.env and os.environ[k] == OLD.env[k])
                or (
                    k not in OLD.env
                    and (
                        (
                            OLD.expected[k] is None
                            and k not in os.environ
                        )
                        or (
                            OLD.expected[k] is not None
                            and os.environ.get(k) == OLD.expected[k]
                        )
                    )
                )
            )
            for k in OLD.expected
        )
)
```
```
@icontract.snapshot(lambda: dict(os.environ), name="env")
@icontract.ensure(lambda result, OLD, path, load_defaults: (__import__("importlib").util.find_spec("dotenv") is None and result is False) or (__import__("importlib").util.find_spec("dotenv") is not None and result == ((load_defaults and any(__import__("dotenv").find_dotenv(n, usecwd=True) for n in (".flaskenv", ".env"))) or (path is not None and os.path.isfile(path)))))
@icontract.ensure(lambda OLD: all(OLD.env.get(k) == os.environ.get(k) for k in OLD.env))
@icontract.ensure(lambda OLD: all(isinstance(os.environ[k], str) for k in set(os.environ) - set(OLD.env)))
```
[4, 5, 6, 7, 8, 9, 10, 16, 17, 26, 27, 32]
===== 4 =====
```
     data: dict[str, str | None] = {}
 
     if load_defaults:
-        for default_name in (".flaskenv", ".env"):
+        for default_name in (".FLASKENV", ".env"):
             if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                 continue
 
@@ -63,4 +63,4 @@ 
         os.environ[key] = value
 
-    return bool(data)  # True if at least one env var was loaded.+    return bool(data)  # True if at least one env var was loaded.
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".FLASKENV", ".env"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.

```
===== 5 =====
```
     data: dict[str, str | None] = {}
 
     if load_defaults:
-        for default_name in (".flaskenv", ".env"):
+        for default_name in (".env", ".env"):  # Duplicate file name
             if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                 continue
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".env", ".env"):  # Duplicate file name
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.
```
===== 6 =====
```
     data: dict[str, str | None] = {}
 
     if load_defaults:
-        for default_name in (".flaskenv", ".env"):
+        for default_name in (".env", ".flaskenv"):  # Incorrect order of files
             if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                 continue
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".env", ".flaskenv"):  # Incorrect order of files
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.
```
===== 7 =====
```
     data: dict[str, str | None] = {}
 
     if load_defaults:
-        for default_name in (".flaskenv", ".env"):
+        for default_name in (".flaskenv", ".ENV"):
             if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                 continue
 
@@ -63,4 +63,4 @@ 
         os.environ[key] = value
 
-    return bool(data)  # True if at least one env var was loaded.+    return bool(data)  # True if at least one env var was loaded.
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".flaskenv", ".ENV"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.

```
===== 8 =====
```
     data: dict[str, str | None] = {}
 
     if load_defaults:
-        for default_name in (".flaskenv", ".env"):
+        for default_name in (".flaskenv", "XX.envXX"):
             if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                 continue
 
@@ -63,4 +63,4 @@ 
         os.environ[key] = value
 
-    return bool(data)  # True if at least one env var was loaded.+    return bool(data)  # True if at least one env var was loaded.
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".flaskenv", "XX.envXX"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.

```
===== 9 =====
```
     data: dict[str, str | None] = {}
 
     if load_defaults:
-        for default_name in (".flaskenv", ".env"):
+        for default_name in (".flaskenv", "config.env"):  # Incorrect file name that won't be found
             if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                 continue
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".flaskenv", "config.env"):  # Incorrect file name that won't be found
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.
```
===== 10 =====
```
     data: dict[str, str | None] = {}
 
     if load_defaults:
-        for default_name in (".flaskenv", ".env"):
+        for default_name in ("XX.flaskenvXX", ".env"):
             if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                 continue
 
@@ -63,4 +63,4 @@ 
         os.environ[key] = value
 
-    return bool(data)  # True if at least one env var was loaded.+    return bool(data)  # True if at least one env var was loaded.
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in ("XX.flaskenvXX", ".env"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.

```
===== 16 =====
```
 
     if load_defaults:
         for default_name in (".flaskenv", ".env"):
-            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
+            if not (default_path := dotenv.find_dotenv(usecwd=True)):
                 continue
 
             data |= dotenv.dotenv_values(default_path, encoding="utf-8")
@@ -63,4 +63,4 @@ 
         os.environ[key] = value
 
-    return bool(data)  # True if at least one env var was loaded.+    return bool(data)  # True if at least one env var was loaded.
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".flaskenv", ".env"):
            if not (default_path := dotenv.find_dotenv(usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.

```
===== 17 =====
```
             if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                 continue
 
-            data |= dotenv.dotenv_values(default_path, encoding="utf-8")
+            data = dotenv.dotenv_values(default_path, encoding="utf-8")
 
     if path is not None and os.path.isfile(path):
         data |= dotenv.dotenv_values(path, encoding="utf-8")
@@ -63,4 +63,4 @@ 
         os.environ[key] = value
 
-    return bool(data)  # True if at least one env var was loaded.+    return bool(data)  # True if at least one env var was loaded.
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".flaskenv", ".env"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data = dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.

```
===== 26 =====
```
         data |= dotenv.dotenv_values(path, encoding="utf-8")
 
     for key, value in data.items():
-        if key in os.environ or value is None:
+        if key in os.environ or value is not None:
             continue
 
         os.environ[key] = value
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".flaskenv", ".env"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is not None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.
```
===== 27 =====
```
         data |= dotenv.dotenv_values(path, encoding="utf-8")
 
     for key, value in data.items():
-        if key in os.environ or value is None:
+        if key in os.environ or value is not None:
             continue
 
         os.environ[key] = value
 
-    return bool(data)  # True if at least one env var was loaded.+    return bool(data)  # True if at least one env var was loaded.
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".flaskenv", ".env"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is not None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.

```
===== 32 =====
```
 
     for key, value in data.items():
         if key in os.environ or value is None:
-            continue
+            break
 
         os.environ[key] = value
 
-    return bool(data)  # True if at least one env var was loaded.+    return bool(data)  # True if at least one env var was loaded.
```
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".flaskenv", ".env"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            break

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.

```
