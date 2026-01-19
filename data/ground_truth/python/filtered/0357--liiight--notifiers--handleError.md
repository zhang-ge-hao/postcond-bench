https://github.com/liiight/notifiers/blob/351c048eb1d8fefae7d638cf1ac667a69815c79a/./notifiers/logging.py#L61-L75
```
🈚️

mock util needed

@icontract.ensure(lambda self, record: True)
```
```
@icontract.snapshot(lambda self: dict(self.fallback_defaults) if self.fallback_defaults is not None else None, name="fallback_defaults")
@icontract.snapshot(lambda self: logging.raiseExceptions, name="raise_exceptions")
@icontract.ensure(lambda OLD, self, record: (not (OLD.raise_exceptions and issubclass(sys.exc_info()[0], NotifierException) and self.fallback)) or (self.fallback_defaults is not None and "message" in self.fallback_defaults and self.fallback_defaults["message"] == f"Could not log msg to provider '{self.provider.name}'!\n{sys.exc_info()[1]}"))
@icontract.ensure(lambda OLD, self, record: (OLD.fallback_defaults == self.fallback_defaults) if not (OLD.raise_exceptions and issubclass(sys.exc_info()[0], NotifierException) and self.fallback) else True)
@icontract.ensure(lambda OLD, self, record: True if not (OLD.raise_exceptions and issubclass(sys.exc_info()[0], NotifierException) and self.fallback) else (not hasattr(self.fallback, "call_args") or getattr(self.fallback, "call_args")[1] == self.fallback_defaults))
@icontract.ensure(lambda OLD, self, record: True if not (OLD.raise_exceptions and issubclass(sys.exc_info()[0], NotifierException) and self.fallback) else (not hasattr(self.fallback, "last_notify_kwargs") or getattr(self.fallback, "last_notify_kwargs") == self.fallback_defaults))
@icontract.ensure(lambda OLD, self, record: True if not (OLD.raise_exceptions and issubclass(sys.exc_info()[0], NotifierException) and self.fallback) else (not hasattr(self.fallback, "last_kwargs") or getattr(self.fallback, "last_kwargs") == self.fallback_defaults))
@icontract.ensure(lambda OLD, self, record: True if not (OLD.raise_exceptions and issubclass(sys.exc_info()[0], NotifierException) and self.fallback) else (not hasattr(self.fallback, "last_call_kwargs") or getattr(self.fallback, "last_call_kwargs") == self.fallback_defaults))
```
[9, 10, 11, 12, 13, 14, 15, 16]
===== 9 =====
```
             if issubclass(t, NotifierException) and self.fallback:
                 msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                 self.fallback_defaults["message"] = msg
-                self.fallback.notify(**self.fallback_defaults)
+                self.fallback.notify(**self.defaults)  # Incorrectly uses defaults instead of fallback_defaults
             else:
                 super().handleError(record)
```
```
    def handleError(self, record):
        """
        Handles any errors raised during the :meth:`emit` method. Will only try to pass exceptions to fallback notifier
        (if defined) in case the exception is a sub-class of :exc:`~notifiers.exceptions.NotifierException`

        :param record: :class:`logging.LogRecord`
        """
        if logging.raiseExceptions:
            t, v, tb = sys.exc_info()
            if issubclass(t, NotifierException) and self.fallback:
                msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                self.fallback_defaults["message"] = msg
                self.fallback.notify(**self.defaults)  # Incorrectly uses defaults instead of fallback_defaults
            else:
                super().handleError(record)
```
===== 10 =====
```
             if issubclass(t, NotifierException) and self.fallback:
                 msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                 self.fallback_defaults["message"] = msg
-                self.fallback.notify(**self.fallback_defaults)
+                self.fallback.notify(**self.fallback_defaults, priority="low")  # Adds an irrelevant argument that may not be handled by the fallback provider
             else:
                 super().handleError(record)
```
```
    def handleError(self, record):
        """
        Handles any errors raised during the :meth:`emit` method. Will only try to pass exceptions to fallback notifier
        (if defined) in case the exception is a sub-class of :exc:`~notifiers.exceptions.NotifierException`

        :param record: :class:`logging.LogRecord`
        """
        if logging.raiseExceptions:
            t, v, tb = sys.exc_info()
            if issubclass(t, NotifierException) and self.fallback:
                msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                self.fallback_defaults["message"] = msg
                self.fallback.notify(**self.fallback_defaults, priority="low")  # Adds an irrelevant argument that may not be handled by the fallback provider
            else:
                super().handleError(record)
```
===== 11 =====
```
             if issubclass(t, NotifierException) and self.fallback:
                 msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                 self.fallback_defaults["message"] = msg
-                self.fallback.notify(**self.fallback_defaults)
+                self.fallback.notify(**self.fallback_defaults, raise_on_errors=False)  # Adds an incorrect argument that changes behavior
             else:
                 super().handleError(record)
```
```
    def handleError(self, record):
        """
        Handles any errors raised during the :meth:`emit` method. Will only try to pass exceptions to fallback notifier
        (if defined) in case the exception is a sub-class of :exc:`~notifiers.exceptions.NotifierException`

        :param record: :class:`logging.LogRecord`
        """
        if logging.raiseExceptions:
            t, v, tb = sys.exc_info()
            if issubclass(t, NotifierException) and self.fallback:
                msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                self.fallback_defaults["message"] = msg
                self.fallback.notify(**self.fallback_defaults, raise_on_errors=False)  # Adds an incorrect argument that changes behavior
            else:
                super().handleError(record)
```
===== 12 =====
```
             if issubclass(t, NotifierException) and self.fallback:
                 msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                 self.fallback_defaults["message"] = msg
-                self.fallback.notify(**self.fallback_defaults)
+                self.fallback.notify(**{**self.fallback_defaults, "message": "Fallback message"})  # Overrides the message incorrectly
             else:
                 super().handleError(record)
```
```
    def handleError(self, record):
        """
        Handles any errors raised during the :meth:`emit` method. Will only try to pass exceptions to fallback notifier
        (if defined) in case the exception is a sub-class of :exc:`~notifiers.exceptions.NotifierException`

        :param record: :class:`logging.LogRecord`
        """
        if logging.raiseExceptions:
            t, v, tb = sys.exc_info()
            if issubclass(t, NotifierException) and self.fallback:
                msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                self.fallback_defaults["message"] = msg
                self.fallback.notify(**{**self.fallback_defaults, "message": "Fallback message"})  # Overrides the message incorrectly
            else:
                super().handleError(record)
```
===== 13 =====
```
             if issubclass(t, NotifierException) and self.fallback:
                 msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                 self.fallback_defaults["message"] = msg
-                self.fallback.notify(**self.fallback_defaults)
+                self.fallback.notify(message=self.fallback_defaults.get("message", "Default fallback message"))  # Uses a default message instead of the one from fallback_defaults
             else:
                 super().handleError(record)
```
```
    def handleError(self, record):
        """
        Handles any errors raised during the :meth:`emit` method. Will only try to pass exceptions to fallback notifier
        (if defined) in case the exception is a sub-class of :exc:`~notifiers.exceptions.NotifierException`

        :param record: :class:`logging.LogRecord`
        """
        if logging.raiseExceptions:
            t, v, tb = sys.exc_info()
            if issubclass(t, NotifierException) and self.fallback:
                msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                self.fallback_defaults["message"] = msg
                self.fallback.notify(message=self.fallback_defaults.get("message", "Default fallback message"))  # Uses a default message instead of the one from fallback_defaults
            else:
                super().handleError(record)
```
===== 14 =====
```
                 self.fallback_defaults["message"] = msg
                 self.fallback.notify(**self.fallback_defaults)
             else:
-                super().handleError(record)+                pass
```
```
    def handleError(self, record):
        """
        Handles any errors raised during the :meth:`emit` method. Will only try to pass exceptions to fallback notifier
        (if defined) in case the exception is a sub-class of :exc:`~notifiers.exceptions.NotifierException`

        :param record: :class:`logging.LogRecord`
        """
        if logging.raiseExceptions:
            t, v, tb = sys.exc_info()
            if issubclass(t, NotifierException) and self.fallback:
                msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                self.fallback_defaults["message"] = msg
                self.fallback.notify(**self.fallback_defaults)
            else:
                pass
```
===== 15 =====
```
                 self.fallback_defaults["message"] = msg
                 self.fallback.notify(**self.fallback_defaults)
             else:
-                super().handleError(record)+                print("Error occurred while logging:", record.msg)
```
```
    def handleError(self, record):
        """
        Handles any errors raised during the :meth:`emit` method. Will only try to pass exceptions to fallback notifier
        (if defined) in case the exception is a sub-class of :exc:`~notifiers.exceptions.NotifierException`

        :param record: :class:`logging.LogRecord`
        """
        if logging.raiseExceptions:
            t, v, tb = sys.exc_info()
            if issubclass(t, NotifierException) and self.fallback:
                msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                self.fallback_defaults["message"] = msg
                self.fallback.notify(**self.fallback_defaults)
            else:
                print("Error occurred while logging:", record.msg)
```
===== 16 =====
```
                 self.fallback_defaults["message"] = msg
                 self.fallback.notify(**self.fallback_defaults)
             else:
-                super().handleError(record)+                return None
```
```
    def handleError(self, record):
        """
        Handles any errors raised during the :meth:`emit` method. Will only try to pass exceptions to fallback notifier
        (if defined) in case the exception is a sub-class of :exc:`~notifiers.exceptions.NotifierException`

        :param record: :class:`logging.LogRecord`
        """
        if logging.raiseExceptions:
            t, v, tb = sys.exc_info()
            if issubclass(t, NotifierException) and self.fallback:
                msg = f"Could not log msg to provider '{self.provider.name}'!\n{v}"
                self.fallback_defaults["message"] = msg
                self.fallback.notify(**self.fallback_defaults)
            else:
                return None
```
