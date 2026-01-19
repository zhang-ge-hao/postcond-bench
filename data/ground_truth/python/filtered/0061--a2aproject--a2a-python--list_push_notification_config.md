https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/server/request_handlers/jsonrpc_handler.py#L362-L392
```
🈚️

async
```
```
@icontract.snapshot(lambda self: getattr(self.request_handler.on_list_task_push_notification_config, "call_args", None), name="handler_call_args")
@icontract.snapshot(lambda self: getattr(self.request_handler.on_list_task_push_notification_config, "return_value", None), name="handler_return")
@icontract.snapshot(lambda self: getattr(self.request_handler.on_list_task_push_notification_config, "side_effect", None), name="handler_side_effect")
@icontract.ensure(
    lambda OLD, result, self, request, context: (
        # handler must have been invoked with the exact (params, context)
        OLD.handler_call_args is not None
        and getattr(OLD.handler_call_args, "args", None) == (request.params, context)
        and (
            # If the handler raised a ServerError, the response must be an error with the same mapping
            (isinstance(OLD.handler_side_effect, ServerError)
             and isinstance(result, ListTaskPushNotificationConfigResponse)
             and isinstance(result.root, JSONRPCErrorResponse)
             and result.root.id == request.id
             and result.root.error == (
                 OLD.handler_side_effect.error
                 if getattr(OLD.handler_side_effect, "error", None)
                 else InternalError()
             )
            )
            or
            # Otherwise the response must be a success wrapper whose result is exactly the handler return object,
            # must be a list and must contain TaskPushNotificationConfig items.
            (not isinstance(OLD.handler_side_effect, ServerError)
             and isinstance(result, ListTaskPushNotificationConfigResponse)
             and isinstance(result.root, ListTaskPushNotificationConfigSuccessResponse)
             and result.root.id == request.id
             and result.root.result is OLD.handler_return
             and isinstance(result.root.result, list)
             and all(isinstance(i, TaskPushNotificationConfig) for i in result.root.result)
            )
        )
    )
)
```
[0, 1, 2, 3, 4]
===== 0 =====
```
             A `ListTaskPushNotificationConfigResponse` object containing the config or a JSON-RPC error.
         """
         try:
-            config = await self.request_handler.on_list_task_push_notification_config(
-                request.params, context
-            )
+            config = None
             return prepare_response_object(
                 request.id,
                 config,
@@ -28,4 +26,4 @@                 root=JSONRPCErrorResponse(
                     id=request.id, error=e.error if e.error else InternalError()
                 )
-            )+            )
```
```
    async def list_push_notification_config(
        self,
        request: ListTaskPushNotificationConfigRequest,
        context: ServerCallContext | None = None,
    ) -> ListTaskPushNotificationConfigResponse:
        """Handles the 'tasks/pushNotificationConfig/list' JSON-RPC method.

        Args:
            request: The incoming `ListTaskPushNotificationConfigRequest` object.
            context: Context provided by the server.

        Returns:
            A `ListTaskPushNotificationConfigResponse` object containing the config or a JSON-RPC error.
        """
        try:
            config = None
            return prepare_response_object(
                request.id,
                config,
                (list,),
                ListTaskPushNotificationConfigSuccessResponse,
                ListTaskPushNotificationConfigResponse,
            )
        except ServerError as e:
            return ListTaskPushNotificationConfigResponse(
                root=JSONRPCErrorResponse(
                    id=request.id, error=e.error if e.error else InternalError()
                )
            )

```
===== 1 =====
```
             )
             return prepare_response_object(
                 request.id,
-                config,
+                None,
                 (list,),
                 ListTaskPushNotificationConfigSuccessResponse,
                 ListTaskPushNotificationConfigResponse,
```
```
    async def list_push_notification_config(
        self,
        request: ListTaskPushNotificationConfigRequest,
        context: ServerCallContext | None = None,
    ) -> ListTaskPushNotificationConfigResponse:
        """Handles the 'tasks/pushNotificationConfig/list' JSON-RPC method.

        Args:
            request: The incoming `ListTaskPushNotificationConfigRequest` object.
            context: Context provided by the server.

        Returns:
            A `ListTaskPushNotificationConfigResponse` object containing the config or a JSON-RPC error.
        """
        try:
            config = await self.request_handler.on_list_task_push_notification_config(
                request.params, context
            )
            return prepare_response_object(
                request.id,
                None,
                (list,),
                ListTaskPushNotificationConfigSuccessResponse,
                ListTaskPushNotificationConfigResponse,
            )
        except ServerError as e:
            return ListTaskPushNotificationConfigResponse(
                root=JSONRPCErrorResponse(
                    id=request.id, error=e.error if e.error else InternalError()
                )
            )
```
===== 2 =====
```
             )
             return prepare_response_object(
                 request.id,
-                config,
+                None,
                 (list,),
                 ListTaskPushNotificationConfigSuccessResponse,
                 ListTaskPushNotificationConfigResponse,
@@ -28,4 +28,4 @@                 root=JSONRPCErrorResponse(
                     id=request.id, error=e.error if e.error else InternalError()
                 )
-            )+            )
```
```
    async def list_push_notification_config(
        self,
        request: ListTaskPushNotificationConfigRequest,
        context: ServerCallContext | None = None,
    ) -> ListTaskPushNotificationConfigResponse:
        """Handles the 'tasks/pushNotificationConfig/list' JSON-RPC method.

        Args:
            request: The incoming `ListTaskPushNotificationConfigRequest` object.
            context: Context provided by the server.

        Returns:
            A `ListTaskPushNotificationConfigResponse` object containing the config or a JSON-RPC error.
        """
        try:
            config = await self.request_handler.on_list_task_push_notification_config(
                request.params, context
            )
            return prepare_response_object(
                request.id,
                None,
                (list,),
                ListTaskPushNotificationConfigSuccessResponse,
                ListTaskPushNotificationConfigResponse,
            )
        except ServerError as e:
            return ListTaskPushNotificationConfigResponse(
                root=JSONRPCErrorResponse(
                    id=request.id, error=e.error if e.error else InternalError()
                )
            )

```
===== 3 =====
```
             )
             return prepare_response_object(
                 request.id,
-                config,
+                config[0],  # Assuming config is a list, this will cause an IndexError if it's empty
                 (list,),
                 ListTaskPushNotificationConfigSuccessResponse,
                 ListTaskPushNotificationConfigResponse,
```
```
    async def list_push_notification_config(
        self,
        request: ListTaskPushNotificationConfigRequest,
        context: ServerCallContext | None = None,
    ) -> ListTaskPushNotificationConfigResponse:
        """Handles the 'tasks/pushNotificationConfig/list' JSON-RPC method.

        Args:
            request: The incoming `ListTaskPushNotificationConfigRequest` object.
            context: Context provided by the server.

        Returns:
            A `ListTaskPushNotificationConfigResponse` object containing the config or a JSON-RPC error.
        """
        try:
            config = await self.request_handler.on_list_task_push_notification_config(
                request.params, context
            )
            return prepare_response_object(
                request.id,
                config[0],  # Assuming config is a list, this will cause an IndexError if it's empty
                (list,),
                ListTaskPushNotificationConfigSuccessResponse,
                ListTaskPushNotificationConfigResponse,
            )
        except ServerError as e:
            return ListTaskPushNotificationConfigResponse(
                root=JSONRPCErrorResponse(
                    id=request.id, error=e.error if e.error else InternalError()
                )
            )
```
===== 4 =====
```
             )
             return prepare_response_object(
                 request.id,
-                config,
+                config[1:],  # This will skip the first element of the config list, potentially losing data
                 (list,),
                 ListTaskPushNotificationConfigSuccessResponse,
                 ListTaskPushNotificationConfigResponse,
```
```
    async def list_push_notification_config(
        self,
        request: ListTaskPushNotificationConfigRequest,
        context: ServerCallContext | None = None,
    ) -> ListTaskPushNotificationConfigResponse:
        """Handles the 'tasks/pushNotificationConfig/list' JSON-RPC method.

        Args:
            request: The incoming `ListTaskPushNotificationConfigRequest` object.
            context: Context provided by the server.

        Returns:
            A `ListTaskPushNotificationConfigResponse` object containing the config or a JSON-RPC error.
        """
        try:
            config = await self.request_handler.on_list_task_push_notification_config(
                request.params, context
            )
            return prepare_response_object(
                request.id,
                config[1:],  # This will skip the first element of the config list, potentially losing data
                (list,),
                ListTaskPushNotificationConfigSuccessResponse,
                ListTaskPushNotificationConfigResponse,
            )
        except ServerError as e:
            return ListTaskPushNotificationConfigResponse(
                root=JSONRPCErrorResponse(
                    id=request.id, error=e.error if e.error else InternalError()
                )
            )
```
