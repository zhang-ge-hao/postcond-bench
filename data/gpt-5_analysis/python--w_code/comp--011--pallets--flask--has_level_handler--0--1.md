https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/logging.py#L31-L47
```
@icontract.snapshot(lambda logger: list(logger.handlers), name="handlers")
@icontract.snapshot(lambda logger: logger.propagate, name="propagate")
@icontract.snapshot(lambda logger: logger.getEffectiveLevel(), name="level")
@icontract.ensure(lambda OLD, logger: list(logger.handlers) == OLD.handlers)
@icontract.ensure(lambda OLD, logger: logger.propagate == OLD.propagate)
@icontract.ensure(lambda OLD, logger: logger.getEffectiveLevel() == OLD.level)
@icontract.ensure(lambda logger, result: not any(h.level <= logger.getEffectiveLevel() for h in logger.handlers) or result)
@icontract.ensure(lambda logger, result: logger.propagate or (result == any(h.level <= logger.getEffectiveLevel() for h in logger.handlers)))
@icontract.ensure(lambda logger, result: (not result) or (any(h.level <= logger.getEffectiveLevel() for h in logger.handlers) or logger.propagate))
```
```
Branch Missed.
```
passed
```
@icontract.ensure(lambda result, logger: (level := logger.getEffectiveLevel()) is not None and (cur := logger) is not None and result == any(((match := (cur is not None and any(handler.level <= level for handler in cur.handlers))), (cur := (cur.parent if cur and cur.propagate else None)), match)[2] for _ in range(1000)))
```
===== 1 =====
failed
```
     level = logger.getEffectiveLevel()
     current = logger
 
-    while current:
+    while current and current.handlers:
         if any(handler.level <= level for handler in current.handlers):
             return True
```
```
def has_level_handler(logger: logging.Logger) -> bool:
    """Check if there is a handler in the logging chain that will handle the
    given logger's :meth:`effective level <~logging.Logger.getEffectiveLevel>`.
    """
    level = logger.getEffectiveLevel()
    current = logger

    while current and current.handlers:
        if any(handler.level <= level for handler in current.handlers):
            return True

        if not current.propagate:
            break

        current = current.parent  # type: ignore

    return False
```
