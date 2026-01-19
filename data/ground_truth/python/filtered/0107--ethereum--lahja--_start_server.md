https://github.com/ethereum/lahja/blob/f51c0b738a7dfd8b2b08a021cb31849792422625/./lahja/asyncio/endpoint.py#L449-L468
```
🈚️

async
```
```
@icontract.snapshot(lambda ipc_path: str(ipc_path), name="expected_ipc_str")
@icontract.ensure(lambda OLD, self: self.is_serving)
@icontract.ensure(lambda OLD, self: self._ipc_path is not None)
@icontract.ensure(lambda OLD, self: str(self.ipc_path) == OLD.expected_ipc_str)
@icontract.ensure(lambda OLD, self: getattr(self, "_server", None) is not None)
@icontract.ensure(
    lambda OLD, self: getattr(self._server, "sockets", None)
    and any(getattr(sock, "getsockname")() == OLD.expected_ipc_str if callable(getattr(sock, "getsockname", None)) else sock.getsockname() == OLD.expected_ipc_str for sock in self._server.sockets)
)
```
[0, 1, 2, 3, 4]
===== 0 =====
```
         elif self.is_serving:
             raise RuntimeError(f"Endpoint {self.name} is already serving")
 
-        self._ipc_path = ipc_path
+        self._ipc_path = None
 
         self._serving = True
 
         self._server = await asyncio.start_unix_server(
             self._accept_conn, path=str(self.ipc_path)
         )
-        self.logger.debug("Endpoint[%s]: server started", self.name)+        self.logger.debug("Endpoint[%s]: server started", self.name)
```
```
    @check_event_loop
    async def _start_server(self, ipc_path: Path) -> None:
        """
        Start serving this :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` so that it
        can receive events. Await until the
        :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` is ready.
        """
        if not self.is_running:
            raise RuntimeError(f"Endpoint {self.name} must be running to start server")
        elif self.is_serving:
            raise RuntimeError(f"Endpoint {self.name} is already serving")

        self._ipc_path = None

        self._serving = True

        self._server = await asyncio.start_unix_server(
            self._accept_conn, path=str(self.ipc_path)
        )
        self.logger.debug("Endpoint[%s]: server started", self.name)

```
===== 1 =====
```
 
         self._serving = True
 
-        self._server = await asyncio.start_unix_server(
-            self._accept_conn, path=str(self.ipc_path)
-        )
-        self.logger.debug("Endpoint[%s]: server started", self.name)+        self._server = None
+        self.logger.debug("Endpoint[%s]: server started", self.name)
```
```
    @check_event_loop
    async def _start_server(self, ipc_path: Path) -> None:
        """
        Start serving this :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` so that it
        can receive events. Await until the
        :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` is ready.
        """
        if not self.is_running:
            raise RuntimeError(f"Endpoint {self.name} must be running to start server")
        elif self.is_serving:
            raise RuntimeError(f"Endpoint {self.name} is already serving")

        self._ipc_path = ipc_path

        self._serving = True

        self._server = None
        self.logger.debug("Endpoint[%s]: server started", self.name)

```
===== 2 =====
```
         self._serving = True
 
         self._server = await asyncio.start_unix_server(
-            self._accept_conn, path=str(self.ipc_path)
+            self._accept_conn, path=str(None)
         )
-        self.logger.debug("Endpoint[%s]: server started", self.name)+        self.logger.debug("Endpoint[%s]: server started", self.name)
```
```
    @check_event_loop
    async def _start_server(self, ipc_path: Path) -> None:
        """
        Start serving this :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` so that it
        can receive events. Await until the
        :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` is ready.
        """
        if not self.is_running:
            raise RuntimeError(f"Endpoint {self.name} must be running to start server")
        elif self.is_serving:
            raise RuntimeError(f"Endpoint {self.name} is already serving")

        self._ipc_path = ipc_path

        self._serving = True

        self._server = await asyncio.start_unix_server(
            self._accept_conn, path=str(None)
        )
        self.logger.debug("Endpoint[%s]: server started", self.name)

```
===== 3 =====
```
         self._serving = True
 
         self._server = await asyncio.start_unix_server(
-            self._accept_conn, path=str(self.ipc_path)
+            self._accept_conn, path=str(self.ipc_path) + "extra"
         )
         self.logger.debug("Endpoint[%s]: server started", self.name)
```
```
    @check_event_loop
    async def _start_server(self, ipc_path: Path) -> None:
        """
        Start serving this :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` so that it
        can receive events. Await until the
        :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` is ready.
        """
        if not self.is_running:
            raise RuntimeError(f"Endpoint {self.name} must be running to start server")
        elif self.is_serving:
            raise RuntimeError(f"Endpoint {self.name} is already serving")

        self._ipc_path = ipc_path

        self._serving = True

        self._server = await asyncio.start_unix_server(
            self._accept_conn, path=str(self.ipc_path) + "extra"
        )
        self.logger.debug("Endpoint[%s]: server started", self.name)
```
===== 4 =====
```
         self._serving = True
 
         self._server = await asyncio.start_unix_server(
-            self._accept_conn, path=str(self.ipc_path)
+            self._accept_conn, path=str(self.ipc_path)[:-1]
         )
         self.logger.debug("Endpoint[%s]: server started", self.name)
```
```
    @check_event_loop
    async def _start_server(self, ipc_path: Path) -> None:
        """
        Start serving this :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` so that it
        can receive events. Await until the
        :class:`~lahja.endpoint.asyncio.AsyncioEndpoint` is ready.
        """
        if not self.is_running:
            raise RuntimeError(f"Endpoint {self.name} must be running to start server")
        elif self.is_serving:
            raise RuntimeError(f"Endpoint {self.name} is already serving")

        self._ipc_path = ipc_path

        self._serving = True

        self._server = await asyncio.start_unix_server(
            self._accept_conn, path=str(self.ipc_path)[:-1]
        )
        self.logger.debug("Endpoint[%s]: server started", self.name)
```
