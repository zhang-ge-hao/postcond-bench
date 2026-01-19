https://github.com/dbcli/pgcli/blob/f46d8446a34084cc2532041619d1f08bda7213e7/./pgcli/completion_refresher.py#L15-L43
```
🈚️

Previous correct postcond now incorrect.

wrong originally

@icontract.snapshot(lambda self: self.is_refreshing(), name="was_refreshing")
@icontract.snapshot(lambda self: self._completer_thread, name="old_thread")
@icontract.snapshot(lambda self: self._restart_refresh.is_set(), name="old_restart")
@icontract.ensure(lambda OLD, self, executor, result: (executor.is_virtual_database() and result == [(None, None, None, "Auto-completion refresh can't be started.")] and self._completer_thread is OLD.old_thread and self._restart_refresh.is_set() == OLD.old_restart) or (not executor.is_virtual_database()))
@icontract.ensure(lambda OLD, self, result: (bool(OLD.was_refreshing) and result == [(None, None, None, "Auto-completion refresh restarted.")] and self._restart_refresh.is_set() and self._completer_thread is OLD.old_thread) or (not bool(OLD.was_refreshing)))
@icontract.ensure(lambda OLD, self, executor, special, callbacks, history, settings, result: ((not executor.is_virtual_database()) and (not bool(OLD.was_refreshing)) and result == [(None, None, None, "Auto-completion refresh started in the background.")] and self._completer_thread is not None and self._completer_thread is not OLD.old_thread and isinstance(self._completer_thread, threading.Thread) and getattr(self._completer_thread, "daemon", False) is True) or (executor.is_virtual_database() or bool(OLD.was_refreshing)))
@icontract.ensure(lambda OLD, self, executor, special, callbacks, history, settings: (not hasattr(self._bg_refresh, "call_args")) or (self._bg_refresh.call_args == ((executor, special, callbacks, history, settings), {})))
@icontract.ensure(lambda OLD, self, callbacks: (not isinstance(callbacks, list) or len(callbacks) == 0 or not hasattr(callbacks[0], "call_count") or callbacks[0].call_count >= 1) )
```
```
@icontract.snapshot(lambda self: self.is_refreshing(), name="was_refreshing")
@icontract.snapshot(lambda self: self._completer_thread, name="old_thread")
@icontract.snapshot(lambda self: self._restart_refresh.is_set(), name="old_restart")
@icontract.ensure(lambda OLD, self, executor, result: (executor.is_virtual_database() and result == [(None, None, None, "Auto-completion refresh can't be started.")] and self._completer_thread is OLD.old_thread and self._restart_refresh.is_set() == OLD.old_restart) or (not executor.is_virtual_database()))
@icontract.ensure(lambda OLD, self, result: (bool(OLD.was_refreshing) and result == [(None, None, None, "Auto-completion refresh restarted.")] and self._restart_refresh.is_set() and self._completer_thread is OLD.old_thread) or (not bool(OLD.was_refreshing)))
@icontract.ensure(lambda OLD, self, executor, special, callbacks, history, settings, result: ((not executor.is_virtual_database()) and (not bool(OLD.was_refreshing)) and result == [(None, None, None, "Auto-completion refresh started in the background.")] and self._completer_thread is not None and self._completer_thread is not OLD.old_thread and isinstance(self._completer_thread, threading.Thread) and getattr(self._completer_thread, "daemon", False) is True) or (executor.is_virtual_database() or bool(OLD.was_refreshing)))
@icontract.ensure(lambda OLD, self, executor, special, callbacks, history, settings: (not hasattr(self._bg_refresh, "call_args")) or (self._bg_refresh.call_args == ((executor, special, callbacks, history, settings), {})))
@icontract.ensure(lambda OLD, self, callbacks: (not isinstance(callbacks, list) or len(callbacks) == 0 or not hasattr(callbacks[0], "call_count") or callbacks[0].call_count >= 1) )
```
[21]
===== 21 =====
```
                 name="completion_refresh",
             )
             self._completer_thread.daemon = True
-            self._completer_thread.start()
+            self._completer_thread.run()
             return [(None, None, None, "Auto-completion refresh started in the background.")]
```
```
    def refresh(self, executor, special, callbacks, history=None, settings=None):
        """
        Creates a PGCompleter object and populates it with the relevant
        completion suggestions in a background thread.

        executor - PGExecute object, used to extract the credentials to connect
                   to the database.
        special - PGSpecial object used for creating a new completion object.
        settings - dict of settings for completer object
        callbacks - A function or a list of functions to call after the thread
                    has completed the refresh. The newly created completion
                    object will be passed in as an argument to each callback.
        """
        if executor.is_virtual_database():
            # do nothing
            return [(None, None, None, "Auto-completion refresh can't be started.")]

        if self.is_refreshing():
            self._restart_refresh.set()
            return [(None, None, None, "Auto-completion refresh restarted.")]
        else:
            self._completer_thread = threading.Thread(
                target=self._bg_refresh,
                args=(executor, special, callbacks, history, settings),
                name="completion_refresh",
            )
            self._completer_thread.daemon = True
            self._completer_thread.run()
            return [(None, None, None, "Auto-completion refresh started in the background.")]
```
