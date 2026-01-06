https://github.com/fwkz/riposte/blob/174bded8ccd665556b163e5c5633d0900715740f/./riposte/riposte.py#L219-L231
```
@icontract.snapshot(lambda self: len(self._commands), name="commands_count")
@icontract.snapshot(lambda self: self._printer_thread, name="printer_thread")
@icontract.ensure(lambda self, commands_count: len(self._commands) == commands_count, 
                  "Number of registered commands should not change during processing")
@icontract.ensure(lambda self, printer_thread: self._printer_thread is printer_thread,
                  "Printer thread instance should not change during processing")
```
```
limited spec

printer_thread
```
failed
```
@icontract.snapshot(lambda self: {name: getattr(cmd._func, "call_count", None) for name, cmd in self._commands.items()}, name="old_calls")
@icontract.ensure(lambda OLD, self: (all(v is None for v in OLD.old_calls.values())) or (sum((getattr(cmd._func, "call_count", 0) if getattr(cmd._func, "call_count", None) is not None else 0) for cmd in self._commands.values()) > sum((v or 0) for v in OLD.old_calls.values())))
@icontract.snapshot(lambda self: {"split": getattr(self._split_inline_commands, "call_count", None), "parse": getattr(self._parse_line, "call_count", None), "get": getattr(self._get_command, "call_count", None)}, name="old_mocks")
@icontract.ensure(lambda OLD, self: (not (OLD.old_mocks["split"] is not None and OLD.old_mocks["parse"] is not None and OLD.old_mocks["get"] is not None)) or (self._split_inline_commands.call_count == OLD.old_mocks["split"] and self._parse_line.call_count == OLD.old_mocks["parse"] and self._get_command.call_count == OLD.old_mocks["get"]))
@icontract.snapshot(lambda self: getattr(__import__("builtins"), "input").return_value if hasattr(getattr(__import__("builtins"), "input"), "return_value") else None, name="input_value")
@icontract.ensure(lambda OLD, self: (OLD.input_value is None) or (getattr(self._split_inline_commands, "call_count", None) is not None) or (getattr(self._get_command, "call_count", None) is None) or (len(self._split_inline_commands(OLD.input_value)) == self._get_command.call_count == getattr(self._get_command.return_value, "execute").call_count))
```
