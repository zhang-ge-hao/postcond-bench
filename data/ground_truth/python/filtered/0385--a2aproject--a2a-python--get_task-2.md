https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/server/tasks/task_manager.py#L62-L88
```
🈚️

async
```
```
@icontract.snapshot(lambda self: self.task_id, name='old_task_id')
@icontract.snapshot(lambda self: self._current_task, name='old_current_task')
@icontract.snapshot(lambda self: self._call_context, name='old_call_context')
@icontract.snapshot(lambda self: getattr(self.task_store.get, "call_count", 0), name='old_call_count')
@icontract.ensure(lambda OLD, self, result: OLD.old_task_id or (result is None and getattr(self.task_store.get, "call_count", 0) == OLD.old_call_count and self._current_task is OLD.old_current_task))
@icontract.ensure(lambda OLD, self, result: (not OLD.old_current_task) or (result is OLD.old_current_task and getattr(self.task_store.get, "call_count", 0) == OLD.old_call_count and self._current_task is OLD.old_current_task))
@icontract.ensure(lambda OLD, self, result: (not (OLD.old_task_id and not OLD.old_current_task)) or (getattr(self.task_store.get, "call_count", 0) == OLD.old_call_count + 1 and getattr(self.task_store.get, "call_args", None) is not None and getattr(self.task_store.get, "call_args").args == (OLD.old_task_id, OLD.old_call_context) and self._current_task is result))
@icontract.ensure(lambda OLD, self, result: self._current_task is result)
```
[0, 1, 2, 3, 4, 5, 6, 7, 8]
===== 0 =====
```
         Returns:
             The `Task` object if found, otherwise `None`.
         """
-        if not self.task_id:
+        if self.task_id == "":
             logger.debug('task_id is not set, cannot get task.')
             return None
```
```
    async def get_task(self) -> Task | None:
        """Retrieves the current task object, either from memory or the store.

        If `task_id` is set, it first checks the in-memory `_current_task`,
        then attempts to load it from the `task_store`.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        if self.task_id == "":
            logger.debug('task_id is not set, cannot get task.')
            return None

        if self._current_task:
            return self._current_task

        logger.debug(
            'Attempting to get task from store with id: %s', self.task_id
        )
        self._current_task = await self.task_store.get(
            self.task_id, self._call_context
        )
        if self._current_task:
            logger.debug('Task %s retrieved successfully.', self.task_id)
        else:
            logger.debug('Task %s not found.', self.task_id)
        return self._current_task
```
===== 1 =====
```
         Returns:
             The `Task` object if found, otherwise `None`.
         """
-        if not self.task_id:
+        if self.task_id == "invalid":
             logger.debug('task_id is not set, cannot get task.')
             return None
```
```
    async def get_task(self) -> Task | None:
        """Retrieves the current task object, either from memory or the store.

        If `task_id` is set, it first checks the in-memory `_current_task`,
        then attempts to load it from the `task_store`.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        if self.task_id == "invalid":
            logger.debug('task_id is not set, cannot get task.')
            return None

        if self._current_task:
            return self._current_task

        logger.debug(
            'Attempting to get task from store with id: %s', self.task_id
        )
        self._current_task = await self.task_store.get(
            self.task_id, self._call_context
        )
        if self._current_task:
            logger.debug('Task %s retrieved successfully.', self.task_id)
        else:
            logger.debug('Task %s not found.', self.task_id)
        return self._current_task
```
===== 2 =====
```
         Returns:
             The `Task` object if found, otherwise `None`.
         """
-        if not self.task_id:
+        if self.task_id and self.task_id == "default":
             logger.debug('task_id is not set, cannot get task.')
             return None
```
```
    async def get_task(self) -> Task | None:
        """Retrieves the current task object, either from memory or the store.

        If `task_id` is set, it first checks the in-memory `_current_task`,
        then attempts to load it from the `task_store`.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        if self.task_id and self.task_id == "default":
            logger.debug('task_id is not set, cannot get task.')
            return None

        if self._current_task:
            return self._current_task

        logger.debug(
            'Attempting to get task from store with id: %s', self.task_id
        )
        self._current_task = await self.task_store.get(
            self.task_id, self._call_context
        )
        if self._current_task:
            logger.debug('Task %s retrieved successfully.', self.task_id)
        else:
            logger.debug('Task %s not found.', self.task_id)
        return self._current_task
```
===== 3 =====
```
         Returns:
             The `Task` object if found, otherwise `None`.
         """
-        if not self.task_id:
+        if self.task_id is not None:
             logger.debug('task_id is not set, cannot get task.')
             return None
```
```
    async def get_task(self) -> Task | None:
        """Retrieves the current task object, either from memory or the store.

        If `task_id` is set, it first checks the in-memory `_current_task`,
        then attempts to load it from the `task_store`.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        if self.task_id is not None:
            logger.debug('task_id is not set, cannot get task.')
            return None

        if self._current_task:
            return self._current_task

        logger.debug(
            'Attempting to get task from store with id: %s', self.task_id
        )
        self._current_task = await self.task_store.get(
            self.task_id, self._call_context
        )
        if self._current_task:
            logger.debug('Task %s retrieved successfully.', self.task_id)
        else:
            logger.debug('Task %s not found.', self.task_id)
        return self._current_task
```
===== 4 =====
```
         Returns:
             The `Task` object if found, otherwise `None`.
         """
-        if not self.task_id:
+        if self.task_id:
             logger.debug('task_id is not set, cannot get task.')
             return None
 
@@ -24,4 +24,4 @@             logger.debug('Task %s retrieved successfully.', self.task_id)
         else:
             logger.debug('Task %s not found.', self.task_id)
-        return self._current_task+        return self._current_task
```
```
    async def get_task(self) -> Task | None:
        """Retrieves the current task object, either from memory or the store.

        If `task_id` is set, it first checks the in-memory `_current_task`,
        then attempts to load it from the `task_store`.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        if self.task_id:
            logger.debug('task_id is not set, cannot get task.')
            return None

        if self._current_task:
            return self._current_task

        logger.debug(
            'Attempting to get task from store with id: %s', self.task_id
        )
        self._current_task = await self.task_store.get(
            self.task_id, self._call_context
        )
        if self._current_task:
            logger.debug('Task %s retrieved successfully.', self.task_id)
        else:
            logger.debug('Task %s not found.', self.task_id)
        return self._current_task

```
===== 5 =====
```
             logger.debug('task_id is not set, cannot get task.')
             return None
 
-        if self._current_task:
+        if not self._current_task and self.task_store:
             return self._current_task
 
         logger.debug(
```
```
    async def get_task(self) -> Task | None:
        """Retrieves the current task object, either from memory or the store.

        If `task_id` is set, it first checks the in-memory `_current_task`,
        then attempts to load it from the `task_store`.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        if not self.task_id:
            logger.debug('task_id is not set, cannot get task.')
            return None

        if not self._current_task and self.task_store:
            return self._current_task

        logger.debug(
            'Attempting to get task from store with id: %s', self.task_id
        )
        self._current_task = await self.task_store.get(
            self.task_id, self._call_context
        )
        if self._current_task:
            logger.debug('Task %s retrieved successfully.', self.task_id)
        else:
            logger.debug('Task %s not found.', self.task_id)
        return self._current_task
```
===== 6 =====
```
             logger.debug('task_id is not set, cannot get task.')
             return None
 
-        if self._current_task:
+        if self._current_task is None:
             return self._current_task
 
         logger.debug(
```
```
    async def get_task(self) -> Task | None:
        """Retrieves the current task object, either from memory or the store.

        If `task_id` is set, it first checks the in-memory `_current_task`,
        then attempts to load it from the `task_store`.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        if not self.task_id:
            logger.debug('task_id is not set, cannot get task.')
            return None

        if self._current_task is None:
            return self._current_task

        logger.debug(
            'Attempting to get task from store with id: %s', self.task_id
        )
        self._current_task = await self.task_store.get(
            self.task_id, self._call_context
        )
        if self._current_task:
            logger.debug('Task %s retrieved successfully.', self.task_id)
        else:
            logger.debug('Task %s not found.', self.task_id)
        return self._current_task
```
===== 7 =====
```
             logger.debug('task_id is not set, cannot get task.')
             return None
 
-        if self._current_task:
+        if self.task_id is None:
             return self._current_task
 
         logger.debug(
```
```
    async def get_task(self) -> Task | None:
        """Retrieves the current task object, either from memory or the store.

        If `task_id` is set, it first checks the in-memory `_current_task`,
        then attempts to load it from the `task_store`.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        if not self.task_id:
            logger.debug('task_id is not set, cannot get task.')
            return None

        if self.task_id is None:
            return self._current_task

        logger.debug(
            'Attempting to get task from store with id: %s', self.task_id
        )
        self._current_task = await self.task_store.get(
            self.task_id, self._call_context
        )
        if self._current_task:
            logger.debug('Task %s retrieved successfully.', self.task_id)
        else:
            logger.debug('Task %s not found.', self.task_id)
        return self._current_task
```
===== 8 =====
```
         logger.debug(
             'Attempting to get task from store with id: %s', self.task_id
         )
-        self._current_task = await self.task_store.get(
-            self.task_id, self._call_context
-        )
+        self._current_task = None
         if self._current_task:
             logger.debug('Task %s retrieved successfully.', self.task_id)
         else:
             logger.debug('Task %s not found.', self.task_id)
-        return self._current_task+        return self._current_task
```
```
    async def get_task(self) -> Task | None:
        """Retrieves the current task object, either from memory or the store.

        If `task_id` is set, it first checks the in-memory `_current_task`,
        then attempts to load it from the `task_store`.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        if not self.task_id:
            logger.debug('task_id is not set, cannot get task.')
            return None

        if self._current_task:
            return self._current_task

        logger.debug(
            'Attempting to get task from store with id: %s', self.task_id
        )
        self._current_task = None
        if self._current_task:
            logger.debug('Task %s retrieved successfully.', self.task_id)
        else:
            logger.debug('Task %s not found.', self.task_id)
        return self._current_task

```
