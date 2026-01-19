https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/testing.py#L275-L298
```
🈚️

_KWARGS cannot access arg dict after the method runs.

mock util needed

@icontract.snapshot(lambda _KWARGS: dict(_KWARGS), name="kwargs_before")
@icontract.ensure(
    lambda result: isinstance(result, Result),
    "invoke must always return a click.testing.Result.",
)
@icontract.ensure(
    lambda self, _KWARGS, OLD:
        # 如果用户自己传了 obj，就不做强制要求
        ("obj" in OLD.kwargs_before)
        or (
            # 否则，必须自动填充 obj
            ("obj" in _KWARGS)
            and isinstance(_KWARGS["obj"], ScriptInfo)
            # 且这个 ScriptInfo 要能加载出正在测试的 app
            and (_KWARGS["obj"].load_app() is self.app)
        ),
    "If no 'obj' argument is given, a ScriptInfo that loads self.app "
    "must be passed as 'obj'.",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
===== 0 =====
```
         if cli is None:
             cli = self.app.cli
 
-        if "obj" not in kwargs:
+        if "OBJ" not in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "OBJ" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs)

```
===== 1 =====
```
         if cli is None:
             cli = self.app.cli
 
-        if "obj" not in kwargs:
+        if "XXobjXX" not in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "XXobjXX" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs)

```
===== 2 =====
```
         if cli is None:
             cli = self.app.cli
 
-        if "obj" not in kwargs:
+        if "obj" in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
         return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs)
```
===== 3 =====
```
         if cli is None:
             cli = self.app.cli
 
-        if "obj" not in kwargs:
+        if "obj" in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs)

```
===== 4 =====
```
         if cli is None:
             cli = self.app.cli
 
-        if "obj" not in kwargs:
+        if "obj" not in kwargs and args is not None:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
         return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs and args is not None:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs)
```
===== 5 =====
```
             cli = self.app.cli
 
         if "obj" not in kwargs:
-            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
+            kwargs["OBJ"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["OBJ"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs)

```
===== 6 =====
```
             cli = self.app.cli
 
         if "obj" not in kwargs:
-            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
+            kwargs["XXobjXX"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["XXobjXX"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs)

```
===== 7 =====
```
             cli = self.app.cli
 
         if "obj" not in kwargs:
-            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
+            kwargs["obj"] = None
 
         return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = None

        return super().invoke(cli, args, **kwargs)
```
===== 8 =====
```
             cli = self.app.cli
 
         if "obj" not in kwargs:
-            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
+            kwargs["obj"] = None
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = None

        return super().invoke(cli, args, **kwargs)

```
===== 9 =====
```
             cli = self.app.cli
 
         if "obj" not in kwargs:
-            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
+            kwargs["obj"] = ScriptInfo(create_app=None)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=None)

        return super().invoke(cli, args, **kwargs)

```
===== 10 =====
```
             cli = self.app.cli
 
         if "obj" not in kwargs:
-            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
+            kwargs["obj"] = ScriptInfo(create_app=lambda: None)
 
         return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: None)

        return super().invoke(cli, args, **kwargs)
```
===== 11 =====
```
             cli = self.app.cli
 
         if "obj" not in kwargs:
-            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
+            kwargs["obj"] = ScriptInfo(create_app=lambda: None)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: None)

        return super().invoke(cli, args, **kwargs)

```
===== 12 =====
```
         if "obj" not in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return None  # This will cause the function to return None instead of the expected Result object
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return None  # This will cause the function to return None instead of the expected Result object
```
===== 13 =====
```
         if "obj" not in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, **kwargs)

```
===== 14 =====
```
         if "obj" not in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, None, **kwargs)
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, None, **kwargs)

```
===== 15 =====
```
         if "obj" not in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, )
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, )

```
===== 16 =====
```
         if "obj" not in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs) if args else None
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs) if args else None
```
===== 17 =====
```
         if "obj" not in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs).exit_code  # Returns only the exit code instead of the Result object
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs).exit_code  # Returns only the exit code instead of the Result object
```
===== 18 =====
```
         if "obj" not in kwargs:
             kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)
 
-        return super().invoke(cli, args, **kwargs)+        return super().invoke(cli, args, **kwargs).output
```
```
    def invoke(  # type: ignore
        self, cli: t.Any = None, args: t.Any = None, **kwargs: t.Any
    ) -> Result:
        """Invokes a CLI command in an isolated environment. See
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.

        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.

        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.

        :return: a :class:`~click.testing.Result` object.
        """
        if cli is None:
            cli = self.app.cli

        if "obj" not in kwargs:
            kwargs["obj"] = ScriptInfo(create_app=lambda: self.app)

        return super().invoke(cli, args, **kwargs).output
```
