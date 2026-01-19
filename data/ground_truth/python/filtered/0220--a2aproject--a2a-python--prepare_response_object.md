https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/server/request_handlers/response_helpers.py#L101-L142
```
🈚️

It's hard

@icontract.ensure(
    lambda result,
           request_id,
           response,
           success_response_types,
           success_payload_type,
           response_type:
        result
        == (
            # 成功分支：response 是 success_response_types 之一
            response_type(
                root=success_payload_type(
                    id=request_id,
                    result=response,
                )
            )
            if isinstance(response, success_response_types)
            else (
                # 失败分支：重新“内联” build_error_response 的逻辑

                # 先算出 JSONRPCErrorResponse.error 应该是什么：
                # - response 是 JSONRPCError: 直接就是它本身
                # - response 是 A2AError: 取它的 root
                # - 否则：是 invalid-agent 的 InvalidAgentResponseError
                response_type(
                    JSONRPCErrorResponse(
                        id=request_id,
                        error=(
                            response
                            if isinstance(response, JSONRPCError)
                            else (
                                response.root
                                if isinstance(response, A2AError)
                                else InvalidAgentResponseError(
                                    message='Agent returned invalid type response for this method'
                                )
                            )
                        ),
                    )
                )
            )
        )
)
```
```
@icontract.snapshot(lambda response: response, name="resp_old")
@icontract.ensure(lambda result: hasattr(result, "root"))
@icontract.ensure(lambda result, OLD, success_response_types, success_payload_type, request_id: (not isinstance(OLD.resp_old, success_response_types)) or (isinstance(result.root, success_payload_type) and getattr(result.root, "id", None) == request_id and getattr(result.root, "result", None) == OLD.resp_old))
@icontract.ensure(lambda result, OLD, request_id: (not isinstance(OLD.resp_old, A2AError)) or (isinstance(result.root, JSONRPCErrorResponse) and getattr(result.root, "id", None) == request_id and getattr(result.root, "error", None) == OLD.resp_old.root))
@icontract.ensure(lambda result, OLD, request_id: (not isinstance(OLD.resp_old, JSONRPCError)) or (isinstance(result.root, JSONRPCErrorResponse) and getattr(result.root, "id", None) == request_id and getattr(result.root, "error", None) == OLD.resp_old))
@icontract.ensure(lambda result, OLD, success_response_types, request_id: (isinstance(OLD.resp_old, success_response_types) or isinstance(OLD.resp_old, A2AError) or isinstance(OLD.resp_old, JSONRPCError)) or (isinstance(result.root, JSONRPCErrorResponse) and getattr(result.root, "id", None) == request_id and isinstance(getattr(result.root, "error", None), InvalidAgentResponseError) and getattr(result.root, "error").message == 'Agent returned invalid type response for this method'))
```
[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
===== 6 =====
```
             root=success_payload_type(id=request_id, result=response)  # type:ignore
         )
 
-    if isinstance(response, A2AError | JSONRPCError):
+    if isinstance(None, A2AError | JSONRPCError):
         return build_error_response(request_id, response, response_type)
 
     # If consumer_data is not an expected success type and not an error,
@@ -39,4 +39,4 @@         )
     )
 
-    return build_error_response(request_id, response, response_type)+    return build_error_response(request_id, response, response_type)
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(None, A2AError | JSONRPCError):
        return build_error_response(request_id, response, response_type)

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)

```
===== 7 =====
```
             root=success_payload_type(id=request_id, result=response)  # type:ignore
         )
 
-    if isinstance(response, A2AError | JSONRPCError):
+    if isinstance(response, (A2AError, JSONRPCError)) and isinstance(response, A2AError):  # Redundant check, may lead to confusion
         return build_error_response(request_id, response, response_type)
 
     # If consumer_data is not an expected success type and not an error,
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, (A2AError, JSONRPCError)) and isinstance(response, A2AError):  # Redundant check, may lead to confusion
        return build_error_response(request_id, response, response_type)

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)
```
===== 8 =====
```
             root=success_payload_type(id=request_id, result=response)  # type:ignore
         )
 
-    if isinstance(response, A2AError | JSONRPCError):
+    if isinstance(response, A2AError):  # Only checks for A2AError, missing JSONRPCError
         return build_error_response(request_id, response, response_type)
 
     # If consumer_data is not an expected success type and not an error,
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, A2AError):  # Only checks for A2AError, missing JSONRPCError
        return build_error_response(request_id, response, response_type)

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)
```
===== 9 =====
```
         )
 
     if isinstance(response, A2AError | JSONRPCError):
-        return build_error_response(request_id, response, response_type)
+        return build_error_response(None, response, response_type)
 
     # If consumer_data is not an expected success type and not an error,
     # it's an invalid type of response from the agent for this specific method.
@@ -39,4 +39,4 @@         )
     )
 
-    return build_error_response(request_id, response, response_type)+    return build_error_response(request_id, response, response_type)
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, A2AError | JSONRPCError):
        return build_error_response(None, response, response_type)

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)

```
===== 10 =====
```
         )
 
     if isinstance(response, A2AError | JSONRPCError):
-        return build_error_response(request_id, response, response_type)
+        return build_error_response(None, response, response_type)  # Passing None as request_id
 
     # If consumer_data is not an expected success type and not an error,
     # it's an invalid type of response from the agent for this specific method.
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, A2AError | JSONRPCError):
        return build_error_response(None, response, response_type)  # Passing None as request_id

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)
```
===== 11 =====
```
         )
 
     if isinstance(response, A2AError | JSONRPCError):
-        return build_error_response(request_id, response, response_type)
+        return build_error_response(request_id, None, response_type)
 
     # If consumer_data is not an expected success type and not an error,
     # it's an invalid type of response from the agent for this specific method.
@@ -39,4 +39,4 @@         )
     )
 
-    return build_error_response(request_id, response, response_type)+    return build_error_response(request_id, response, response_type)
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, A2AError | JSONRPCError):
        return build_error_response(request_id, None, response_type)

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)

```
===== 12 =====
```
         )
 
     if isinstance(response, A2AError | JSONRPCError):
-        return build_error_response(request_id, response, response_type)
+        return build_error_response(request_id, response, )
 
     # If consumer_data is not an expected success type and not an error,
     # it's an invalid type of response from the agent for this specific method.
@@ -39,4 +39,4 @@         )
     )
 
-    return build_error_response(request_id, response, response_type)+    return build_error_response(request_id, response, response_type)
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, A2AError | JSONRPCError):
        return build_error_response(request_id, response, )

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)

```
===== 13 =====
```
         )
 
     if isinstance(response, A2AError | JSONRPCError):
-        return build_error_response(request_id, response, response_type)
+        return build_error_response(request_id, response, None)
 
     # If consumer_data is not an expected success type and not an error,
     # it's an invalid type of response from the agent for this specific method.
@@ -39,4 +39,4 @@         )
     )
 
-    return build_error_response(request_id, response, response_type)+    return build_error_response(request_id, response, response_type)
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, A2AError | JSONRPCError):
        return build_error_response(request_id, response, None)

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)

```
===== 14 =====
```
         )
 
     if isinstance(response, A2AError | JSONRPCError):
-        return build_error_response(request_id, response, response_type)
+        return build_error_response(request_id, response, success_payload_type)  # Incorrectly using success_payload_type instead of response_type
 
     # If consumer_data is not an expected success type and not an error,
     # it's an invalid type of response from the agent for this specific method.
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, A2AError | JSONRPCError):
        return build_error_response(request_id, response, success_payload_type)  # Incorrectly using success_payload_type instead of response_type

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)
```
===== 15 =====
```
         )
 
     if isinstance(response, A2AError | JSONRPCError):
-        return build_error_response(request_id, response, response_type)
+        return build_error_response(request_id, response_type)
 
     # If consumer_data is not an expected success type and not an error,
     # it's an invalid type of response from the agent for this specific method.
@@ -39,4 +39,4 @@         )
     )
 
-    return build_error_response(request_id, response, response_type)+    return build_error_response(request_id, response, response_type)
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, A2AError | JSONRPCError):
        return build_error_response(request_id, response_type)

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)

```
===== 16 =====
```
         )
 
     if isinstance(response, A2AError | JSONRPCError):
-        return build_error_response(request_id, response, response_type)
+        return build_error_response(response, response_type)
 
     # If consumer_data is not an expected success type and not an error,
     # it's an invalid type of response from the agent for this specific method.
@@ -39,4 +39,4 @@         )
     )
 
-    return build_error_response(request_id, response, response_type)+    return build_error_response(request_id, response, response_type)
```
```
def prepare_response_object(
    request_id: str | int | None,
    response: EventTypes,
    success_response_types: tuple[type, ...],
    success_payload_type: type[SPT],
    response_type: type[RT],
) -> RT:
    """Helper method to build appropriate JSONRPCResponse object for RPC methods.

    Based on the type of the `response` object received from the handler,
    it constructs either a success response wrapped in the appropriate payload type
    or an error response.

    Args:
        request_id: The ID of the request.
        response: The object received from the request handler.
        success_response_types: A tuple of expected Pydantic model types for a successful result.
        success_payload_type: The Pydantic model type for the success payload
                                (e.g., `SendMessageSuccessResponse`).
        response_type: The Pydantic RootModel type that wraps the final response
                       (e.g., `SendMessageResponse`).

    Returns:
        A Pydantic model representing the final JSON-RPC response (success or error).
    """
    if isinstance(response, success_response_types):
        return response_type(
            root=success_payload_type(id=request_id, result=response)  # type:ignore
        )

    if isinstance(response, A2AError | JSONRPCError):
        return build_error_response(response, response_type)

    # If consumer_data is not an expected success type and not an error,
    # it's an invalid type of response from the agent for this specific method.
    response = A2AError(
        root=InvalidAgentResponseError(
            message='Agent returned invalid type response for this method'
        )
    )

    return build_error_response(request_id, response, response_type)

```
