https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/asgi/multipart.py#L91-L118
```
🈚️

async
```
```
@icontract.snapshot(lambda self: self._media, name='old_media')
@icontract.ensure(lambda result, self: result is self._media)
@icontract.ensure(lambda self, OLD: (OLD.old_media is not _UNSET) or (self._media is not _UNSET))
@icontract.ensure(lambda result, OLD: (OLD.old_media is not _UNSET) or (result is not None))
@icontract.ensure(lambda self, OLD: (OLD.old_media is _UNSET) or (self._media is OLD.old_media))
@icontract.ensure(lambda result, OLD: (OLD.old_media is _UNSET) or (result is OLD.old_media))
```
[0, 1, 2, 3, 4]
===== 0 =====
```
         Returns:
             object: The deserialized media representation.
         """
-        if self._media is _UNSET:
+        if self._media is None:
             handler, _, _ = self._parse_options.media_handlers._resolve(
                 self.content_type, 'text/plain'
             )
```
```
    async def get_media(self) -> Any:
        """Return a deserialized form of the multipart body part.

        When called, this method will attempt to deserialize the body part
        stream using the Content-Type header as well as the media-type handlers
        configured via :class:`~falcon.media.multipart.MultipartParseOptions`.

        The result will be cached and returned in subsequent calls::

            deserialized_media = await part.get_media()

        Returns:
            object: The deserialized media representation.
        """
        if self._media is None:
            handler, _, _ = self._parse_options.media_handlers._resolve(
                self.content_type, 'text/plain'
            )

            try:
                self._media = await handler.deserialize_async(
                    self.stream, self.content_type, None
                )
            finally:
                if handler.exhaust_stream:
                    await self.stream.exhaust()

        return self._media
```
===== 1 =====
```
         Returns:
             object: The deserialized media representation.
         """
-        if self._media is _UNSET:
+        if self._media is _ALLOWED_CONTENT_HEADERS:
             handler, _, _ = self._parse_options.media_handlers._resolve(
                 self.content_type, 'text/plain'
             )
```
```
    async def get_media(self) -> Any:
        """Return a deserialized form of the multipart body part.

        When called, this method will attempt to deserialize the body part
        stream using the Content-Type header as well as the media-type handlers
        configured via :class:`~falcon.media.multipart.MultipartParseOptions`.

        The result will be cached and returned in subsequent calls::

            deserialized_media = await part.get_media()

        Returns:
            object: The deserialized media representation.
        """
        if self._media is _ALLOWED_CONTENT_HEADERS:
            handler, _, _ = self._parse_options.media_handlers._resolve(
                self.content_type, 'text/plain'
            )

            try:
                self._media = await handler.deserialize_async(
                    self.stream, self.content_type, None
                )
            finally:
                if handler.exhaust_stream:
                    await self.stream.exhaust()

        return self._media
```
===== 2 =====
```
         Returns:
             object: The deserialized media representation.
         """
-        if self._media is _UNSET:
+        if self._media is not _UNSET:
             handler, _, _ = self._parse_options.media_handlers._resolve(
                 self.content_type, 'text/plain'
             )
```
```
    async def get_media(self) -> Any:
        """Return a deserialized form of the multipart body part.

        When called, this method will attempt to deserialize the body part
        stream using the Content-Type header as well as the media-type handlers
        configured via :class:`~falcon.media.multipart.MultipartParseOptions`.

        The result will be cached and returned in subsequent calls::

            deserialized_media = await part.get_media()

        Returns:
            object: The deserialized media representation.
        """
        if self._media is not _UNSET:
            handler, _, _ = self._parse_options.media_handlers._resolve(
                self.content_type, 'text/plain'
            )

            try:
                self._media = await handler.deserialize_async(
                    self.stream, self.content_type, None
                )
            finally:
                if handler.exhaust_stream:
                    await self.stream.exhaust()

        return self._media
```
===== 3 =====
```
         Returns:
             object: The deserialized media representation.
         """
-        if self._media is _UNSET:
+        if self._media is not _UNSET:
             handler, _, _ = self._parse_options.media_handlers._resolve(
                 self.content_type, 'text/plain'
             )
@@ -25,4 +25,4 @@                 if handler.exhaust_stream:
                     await self.stream.exhaust()
 
-        return self._media+        return self._media
```
```
    async def get_media(self) -> Any:
        """Return a deserialized form of the multipart body part.

        When called, this method will attempt to deserialize the body part
        stream using the Content-Type header as well as the media-type handlers
        configured via :class:`~falcon.media.multipart.MultipartParseOptions`.

        The result will be cached and returned in subsequent calls::

            deserialized_media = await part.get_media()

        Returns:
            object: The deserialized media representation.
        """
        if self._media is not _UNSET:
            handler, _, _ = self._parse_options.media_handlers._resolve(
                self.content_type, 'text/plain'
            )

            try:
                self._media = await handler.deserialize_async(
                    self.stream, self.content_type, None
                )
            finally:
                if handler.exhaust_stream:
                    await self.stream.exhaust()

        return self._media

```
===== 4 =====
```
             )
 
             try:
-                self._media = await handler.deserialize_async(
-                    self.stream, self.content_type, None
-                )
+                self._media = None
             finally:
                 if handler.exhaust_stream:
                     await self.stream.exhaust()
 
-        return self._media+        return self._media
```
```
    async def get_media(self) -> Any:
        """Return a deserialized form of the multipart body part.

        When called, this method will attempt to deserialize the body part
        stream using the Content-Type header as well as the media-type handlers
        configured via :class:`~falcon.media.multipart.MultipartParseOptions`.

        The result will be cached and returned in subsequent calls::

            deserialized_media = await part.get_media()

        Returns:
            object: The deserialized media representation.
        """
        if self._media is _UNSET:
            handler, _, _ = self._parse_options.media_handlers._resolve(
                self.content_type, 'text/plain'
            )

            try:
                self._media = None
            finally:
                if handler.exhaust_stream:
                    await self.stream.exhaust()

        return self._media

```
