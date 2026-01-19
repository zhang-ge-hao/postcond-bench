https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/server/apps/jsonrpc/jsonrpc_app.py#L546-L572
```
🈚️

async
```
```
@icontract.snapshot(lambda self: self.agent_card, name="orig_agent_card")
@icontract.snapshot(lambda self: self.card_modifier, name="orig_card_modifier")
@icontract.snapshot(lambda self: (self.card_modifier(self.agent_card).model_dump(exclude_none=True, by_alias=True) if callable(self.card_modifier) else self.agent_card.model_dump(exclude_none=True, by_alias=True)), name="expected_body")
@icontract.snapshot(lambda: (__import__("logging").getLogger(__name__).addHandler(h := type("H", (__import__("logging").Handler,), {"records": [], "emit": lambda self, rec: self.records.append(rec)})()), h)[1], name="log_handler")
@icontract.ensure(lambda result: isinstance(result, JSONResponse))
@icontract.ensure(lambda result: result.status_code == 200)
@icontract.ensure(lambda result, expected_body: __import__("json").loads(result.body) == expected_body)
@icontract.ensure(lambda result: "X-Custom-Header" not in result.headers)
@icontract.ensure(lambda request, log_handler: request.url.path != PREV_AGENT_CARD_WELL_KNOWN_PATH or any((rec.levelno == __import__("logging").WARNING and rec.getMessage() == ("Deprecated agent card endpoint '%s' accessed. Please use '%s' instead. This endpoint will be removed in a future version." % (PREV_AGENT_CARD_WELL_KNOWN_PATH, AGENT_CARD_WELL_KNOWN_PATH)))) for rec in log_handler.records)
```
[0, 1, 2, 3, 4, 5]
===== 0 =====
```
             )
 
         card_to_serve = self.agent_card
-        if self.card_modifier:
+        if self.card_modifier == True:
             card_to_serve = self.card_modifier(card_to_serve)
 
         return JSONResponse(
```
```
    async def _handle_get_agent_card(self, request: Request) -> JSONResponse:
        """Handles GET requests for the agent card endpoint.

        Args:
            request: The incoming Starlette Request object.

        Returns:
            A JSONResponse containing the agent card data.
        """
        if request.url.path == PREV_AGENT_CARD_WELL_KNOWN_PATH:
            logger.warning(
                "Deprecated agent card endpoint '%s' accessed. "
                "Please use '%s' instead. This endpoint will be removed in a future version.",
                PREV_AGENT_CARD_WELL_KNOWN_PATH,
                AGENT_CARD_WELL_KNOWN_PATH,
            )

        card_to_serve = self.agent_card
        if self.card_modifier == True:
            card_to_serve = self.card_modifier(card_to_serve)

        return JSONResponse(
            card_to_serve.model_dump(
                exclude_none=True,
                by_alias=True,
            )
        )
```
===== 1 =====
```
             card_to_serve = self.card_modifier(card_to_serve)
 
         return JSONResponse(
-            card_to_serve.model_dump(
-                exclude_none=True,
-                by_alias=True,
-            )
-        )+            None
+        )
```
```
    async def _handle_get_agent_card(self, request: Request) -> JSONResponse:
        """Handles GET requests for the agent card endpoint.

        Args:
            request: The incoming Starlette Request object.

        Returns:
            A JSONResponse containing the agent card data.
        """
        if request.url.path == PREV_AGENT_CARD_WELL_KNOWN_PATH:
            logger.warning(
                "Deprecated agent card endpoint '%s' accessed. "
                "Please use '%s' instead. This endpoint will be removed in a future version.",
                PREV_AGENT_CARD_WELL_KNOWN_PATH,
                AGENT_CARD_WELL_KNOWN_PATH,
            )

        card_to_serve = self.agent_card
        if self.card_modifier:
            card_to_serve = self.card_modifier(card_to_serve)

        return JSONResponse(
            None
        )

```
===== 2 =====
```
 
         return JSONResponse(
             card_to_serve.model_dump(
-                exclude_none=True,
+                include={'field1', 'field2'},
                 by_alias=True,
             )
         )
```
```
    async def _handle_get_agent_card(self, request: Request) -> JSONResponse:
        """Handles GET requests for the agent card endpoint.

        Args:
            request: The incoming Starlette Request object.

        Returns:
            A JSONResponse containing the agent card data.
        """
        if request.url.path == PREV_AGENT_CARD_WELL_KNOWN_PATH:
            logger.warning(
                "Deprecated agent card endpoint '%s' accessed. "
                "Please use '%s' instead. This endpoint will be removed in a future version.",
                PREV_AGENT_CARD_WELL_KNOWN_PATH,
                AGENT_CARD_WELL_KNOWN_PATH,
            )

        card_to_serve = self.agent_card
        if self.card_modifier:
            card_to_serve = self.card_modifier(card_to_serve)

        return JSONResponse(
            card_to_serve.model_dump(
                include={'field1', 'field2'},
                by_alias=True,
            )
        )
```
===== 3 =====
```
         return JSONResponse(
             card_to_serve.model_dump(
                 exclude_none=True,
-                by_alias=True,
+                by_alias=False,
             )
         )
```
```
    async def _handle_get_agent_card(self, request: Request) -> JSONResponse:
        """Handles GET requests for the agent card endpoint.

        Args:
            request: The incoming Starlette Request object.

        Returns:
            A JSONResponse containing the agent card data.
        """
        if request.url.path == PREV_AGENT_CARD_WELL_KNOWN_PATH:
            logger.warning(
                "Deprecated agent card endpoint '%s' accessed. "
                "Please use '%s' instead. This endpoint will be removed in a future version.",
                PREV_AGENT_CARD_WELL_KNOWN_PATH,
                AGENT_CARD_WELL_KNOWN_PATH,
            )

        card_to_serve = self.agent_card
        if self.card_modifier:
            card_to_serve = self.card_modifier(card_to_serve)

        return JSONResponse(
            card_to_serve.model_dump(
                exclude_none=True,
                by_alias=False,
            )
        )
```
===== 4 =====
```
         return JSONResponse(
             card_to_serve.model_dump(
                 exclude_none=True,
-                by_alias=True,
+                by_alias=False,
             )
-        )+        )
```
```
    async def _handle_get_agent_card(self, request: Request) -> JSONResponse:
        """Handles GET requests for the agent card endpoint.

        Args:
            request: The incoming Starlette Request object.

        Returns:
            A JSONResponse containing the agent card data.
        """
        if request.url.path == PREV_AGENT_CARD_WELL_KNOWN_PATH:
            logger.warning(
                "Deprecated agent card endpoint '%s' accessed. "
                "Please use '%s' instead. This endpoint will be removed in a future version.",
                PREV_AGENT_CARD_WELL_KNOWN_PATH,
                AGENT_CARD_WELL_KNOWN_PATH,
            )

        card_to_serve = self.agent_card
        if self.card_modifier:
            card_to_serve = self.card_modifier(card_to_serve)

        return JSONResponse(
            card_to_serve.model_dump(
                exclude_none=True,
                by_alias=False,
            )
        )

```
===== 5 =====
```
         return JSONResponse(
             card_to_serve.model_dump(
                 exclude_none=True,
-                by_alias=True,
+                include={'field1', 'field2'},
             )
         )
```
```
    async def _handle_get_agent_card(self, request: Request) -> JSONResponse:
        """Handles GET requests for the agent card endpoint.

        Args:
            request: The incoming Starlette Request object.

        Returns:
            A JSONResponse containing the agent card data.
        """
        if request.url.path == PREV_AGENT_CARD_WELL_KNOWN_PATH:
            logger.warning(
                "Deprecated agent card endpoint '%s' accessed. "
                "Please use '%s' instead. This endpoint will be removed in a future version.",
                PREV_AGENT_CARD_WELL_KNOWN_PATH,
                AGENT_CARD_WELL_KNOWN_PATH,
            )

        card_to_serve = self.agent_card
        if self.card_modifier:
            card_to_serve = self.card_modifier(card_to_serve)

        return JSONResponse(
            card_to_serve.model_dump(
                exclude_none=True,
                include={'field1', 'field2'},
            )
        )
```
