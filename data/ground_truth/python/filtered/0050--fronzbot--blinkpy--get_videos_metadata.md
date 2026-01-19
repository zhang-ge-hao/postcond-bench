https://github.com/fronzbot/blinkpy/blob/1e868e2a19fa8b364f4e9164d1e31e7e4969c7fb/./blinkpy/blinkpy.py#L372-L402
```
🈚️

async
```
```
@icontract.snapshot(lambda _ARGS, _KWARGS: _KWARGS.get("since", (_ARGS[1] if len(_ARGS) > 1 else None)), name="since_arg")
@icontract.snapshot(lambda _ARGS, _KWARGS: _KWARGS.get("stop", (_ARGS[3] if len(_ARGS) > 3 else 10)), name="stop_arg")
@icontract.snapshot(lambda _ARGS, _KWARGS: _ARGS[0].last_refresh, name="last_refresh")
@icontract.snapshot(lambda _ARGS, _KWARGS: _ARGS[0].api.request_videos, name="request_videos_mock")
@icontract.snapshot(lambda OLD: getattr(OLD.request_videos_mock, "call_args_list", []), name="call_args_list")
@icontract.snapshot(lambda OLD: getattr(OLD.request_videos_mock, "side_effect", None), name="side_effect")
@icontract.snapshot(lambda OLD: (
    (parse(OLD.since_arg, fuzzy=True).timestamp() if OLD.since_arg is not None else OLD.last_refresh)
), name="expected_time")
@icontract.ensure(lambda result: isinstance(result, list))
@icontract.ensure(lambda result: all(isinstance(item, dict) for item in result))
@icontract.ensure(lambda OLD, result: len(OLD.call_args_list) >= 1)
@icontract.ensure(lambda OLD, result: OLD.call_args_list[0][1].get("page") == 1)
@icontract.ensure(lambda OLD, result: all(
    OLD.call_args_list[i][1].get("page") + 1 == OLD.call_args_list[i + 1][1].get("page")
    for i in range(len(OLD.call_args_list) - 1)
))
@icontract.ensure(lambda OLD, result: all(
    call[1].get("time") == OLD.expected_time
    for call in OLD.call_args_list
))
@icontract.ensure(lambda OLD, result: (
    OLD.side_effect is None
    or result == sum((resp.get("media", []) for resp in (OLD.side_effect[:len(OLD.call_args_list)] if isinstance(OLD.side_effect, (list, tuple)) else [])), [])
))
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]
===== 0 =====
```
         """
         videos = []
         if since is None:
-            since_epochs = self.last_refresh
+            since_epochs = None
         else:
             parsed_datetime = parse(since, fuzzy=True)
             since_epochs = parsed_datetime.timestamp()
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = None
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 1 =====
```
             parsed_datetime = parse(since, fuzzy=True)
             since_epochs = parsed_datetime.timestamp()
 
-        formatted_date = util.get_time(time_to_convert=since_epochs)
+        formatted_date = None
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
         for page in range(1, stop):
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = None
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 2 =====
```
             parsed_datetime = parse(since, fuzzy=True)
             since_epochs = parsed_datetime.timestamp()
 
-        formatted_date = util.get_time(time_to_convert=since_epochs)
+        formatted_date = util.get_time(time_to_convert=None)
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
         for page in range(1, stop):
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=None)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 3 =====
```
             parsed_datetime = parse(since, fuzzy=True)
             since_epochs = parsed_datetime.timestamp()
 
-        formatted_date = util.get_time(time_to_convert=since_epochs)
+        formatted_date = util.get_time(time_to_convert=since_epochs + 3600)  # Adds an hour to the timestamp
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
         for page in range(1, stop):
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs + 3600)  # Adds an hour to the timestamp
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 4 =====
```
             parsed_datetime = parse(since, fuzzy=True)
             since_epochs = parsed_datetime.timestamp()
 
-        formatted_date = util.get_time(time_to_convert=since_epochs)
+        formatted_date = util.get_time(time_to_convert=since_epochs - 3600)  # Subtracts an hour from the timestamp
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
         for page in range(1, stop):
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs - 3600)  # Subtracts an hour from the timestamp
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 5 =====
```
             parsed_datetime = parse(since, fuzzy=True)
             since_epochs = parsed_datetime.timestamp()
 
-        formatted_date = util.get_time(time_to_convert=since_epochs)
+        formatted_date = util.get_time(time_to_convert=since_epochs) if since_epochs > 0 else "Invalid date"  # Returns a string if since_epochs is non-positive
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
         for page in range(1, stop):
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs) if since_epochs > 0 else "Invalid date"  # Returns a string if since_epochs is non-positive
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 6 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.debug("Retrieving videos since %s", formatted_date)
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.debug("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 7 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.info("Fetching videos from %s", formatted_date)
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Fetching videos from %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 8 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.info("Retrieving videos since %s", )
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", )

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 9 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.info("Retrieving videos since %s", None)
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", None)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 10 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.info("Retrieving videos since %s", since)
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", since)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 11 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.info("Videos will be retrieved starting from %s", formatted_date)
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Videos will be retrieved starting from %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 12 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.info("XXRetrieving videos since %sXX", formatted_date)
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("XXRetrieving videos since %sXX", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 13 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.info("retrieving videos since %s", formatted_date)
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 14 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.info(formatted_date)
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info(formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 15 =====
```
             since_epochs = parsed_datetime.timestamp()
 
         formatted_date = util.get_time(time_to_convert=since_epochs)
-        _LOGGER.info("Retrieving videos since %s", formatted_date)
+        _LOGGER.warning("Attempting to retrieve videos since %s", formatted_date)
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.warning("Attempting to retrieve videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 16 =====
```
         formatted_date = util.get_time(time_to_convert=since_epochs)
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
-        for page in range(1, stop):
+        for page in range(0, stop):  # Starts from 0 instead of 1, potentially missing the first page of results.
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(0, stop):  # Starts from 0 instead of 1, potentially missing the first page of results.
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 17 =====
```
         formatted_date = util.get_time(time_to_convert=since_epochs)
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
-        for page in range(1, stop):
+        for page in range(1, ):
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, ):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 18 =====
```
         formatted_date = util.get_time(time_to_convert=since_epochs)
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
-        for page in range(1, stop):
+        for page in range(1, stop + 1):  # Includes an extra page, leading to an out-of-bounds request.
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop + 1):  # Includes an extra page, leading to an out-of-bounds request.
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 19 =====
```
         formatted_date = util.get_time(time_to_convert=since_epochs)
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
-        for page in range(1, stop):
+        for page in range(1, stop, -1):  # Incorrect step value, leading to an empty range and no iterations.
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop, -1):  # Incorrect step value, leading to an empty range and no iterations.
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 20 =====
```
         formatted_date = util.get_time(time_to_convert=since_epochs)
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
-        for page in range(1, stop):
+        for page in range(2, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(2, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 21 =====
```
         formatted_date = util.get_time(time_to_convert=since_epochs)
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
-        for page in range(1, stop):
+        for page in range(stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 22 =====
```
         formatted_date = util.get_time(time_to_convert=since_epochs)
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
-        for page in range(1, stop):
+        for page in range(stop):  # Uses stop as the upper limit, which may not correspond to the intended page count.
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(stop):  # Uses stop as the upper limit, which may not correspond to the intended page count.
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 23 =====
```
         _LOGGER.info("Retrieving videos since %s", formatted_date)
 
         for page in range(1, stop):
-            response = await api.request_videos(self, time=since_epochs, page=page)
+            response = None
             _LOGGER.debug("Processing page %s", page)
             try:
                 result = response["media"]
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = None
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 24 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.debug("Currently on page %s", page + 1)
             try:
                 result = response["media"]
                 if not result:
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Currently on page %s", page + 1)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 25 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.debug("Fetching data for page %s", page)
             try:
                 result = response["media"]
                 if not result:
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Fetching data for page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 26 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.debug("Page %s processed successfully", page)
             try:
                 result = response["media"]
                 if not result:
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Page %s processed successfully", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 27 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.debug("Processing page %s", )
             try:
                 result = response["media"]
                 if not result:
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", )
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 28 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.debug("Processing page %s", None)
             try:
                 result = response["media"]
                 if not result:
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", None)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 29 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.debug("XXProcessing page %sXX", page)
             try:
                 result = response["media"]
                 if not result:
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("XXProcessing page %sXX", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 30 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.debug("processing page %s", page)
             try:
                 result = response["media"]
                 if not result:
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 31 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.debug(page)
             try:
                 result = response["media"]
                 if not result:
@@ -28,4 +28,4 @@             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug(page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 32 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.info("Processing page %s", page)
             try:
                 result = response["media"]
                 if not result:
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.info("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 33 =====
```
 
         for page in range(1, stop):
             response = await api.request_videos(self, time=since_epochs, page=page)
-            _LOGGER.debug("Processing page %s", page)
+            _LOGGER.warning("Page %s is being processed", page)
             try:
                 result = response["media"]
                 if not result:
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.warning("Page %s is being processed", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 34 =====
```
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
-                result = response["media"]
+                result = None
                 if not result:
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = None
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 35 =====
```
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
-                result = response["media"]
+                result = response["MEDIA"]
                 if not result:
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["MEDIA"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 36 =====
```
             response = await api.request_videos(self, time=since_epochs, page=page)
             _LOGGER.debug("Processing page %s", page)
             try:
-                result = response["media"]
+                result = response["XXmediaXX"]
                 if not result:
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["XXmediaXX"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 37 =====
```
             _LOGGER.debug("Processing page %s", page)
             try:
                 result = response["media"]
-                if not result:
+                if len(result) < 5:
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if len(result) < 5:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 38 =====
```
             _LOGGER.debug("Processing page %s", page)
             try:
                 result = response["media"]
-                if not result:
+                if result and "media" not in result:
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if result and "media" not in result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 39 =====
```
             _LOGGER.debug("Processing page %s", page)
             try:
                 result = response["media"]
-                if not result:
+                if result:
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 40 =====
```
                 result = response["media"]
                 if not result:
                     raise KeyError
-                videos.extend(result)
+                videos.append(result)
             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.append(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 41 =====
```
                 result = response["media"]
                 if not result:
                     raise KeyError
-                videos.extend(result)
+                videos.extend(None)
             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(None)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos

```
===== 42 =====
```
                 result = response["media"]
                 if not result:
                     raise KeyError
-                videos.extend(result)
+                videos.extend(result[:0])  # Extends with an empty slice
             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
                 break
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result[:0])  # Extends with an empty slice
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                break
        return videos
```
===== 43 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.debug("No videos found on page %s, but we will keep searching.", page)
                 break
         return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.debug("No videos found on page %s, but we will keep searching.", page)
                break
        return videos
```
===== 44 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.error("No videos on page %s, but this is expected.", page)
                 break
         return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.error("No videos on page %s, but this is expected.", page)
                break
        return videos
```
===== 45 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.info("No videos found on page %s. Exiting.", )
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", )
                break
        return videos

```
===== 46 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.info("No videos found on page %s. Exiting.", None)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", None)
                break
        return videos

```
===== 47 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.info("Page %s has no videos, proceeding without any action.", page)
                 break
         return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("Page %s has no videos, proceeding without any action.", page)
                break
        return videos
```
===== 48 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.info("Page %s is empty, but let's check the next one.", page)
                 break
         return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("Page %s is empty, but let's check the next one.", page)
                break
        return videos
```
===== 49 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.info("XXNo videos found on page %s. Exiting.XX", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("XXNo videos found on page %s. Exiting.XX", page)
                break
        return videos

```
===== 50 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.info("no videos found on page %s. exiting.", page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("no videos found on page %s. exiting.", page)
                break
        return videos

```
===== 51 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.info(page)
                 break
-        return videos+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info(page)
                break
        return videos

```
===== 52 =====
```
                     raise KeyError
                 videos.extend(result)
             except (KeyError, TypeError):
-                _LOGGER.info("No videos found on page %s. Exiting.", page)
+                _LOGGER.warning("Page %s returned no videos, continuing to next page.", page)
                 break
         return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.warning("Page %s returned no videos, continuing to next page.", page)
                break
        return videos
```
===== 53 =====
```
                 videos.extend(result)
             except (KeyError, TypeError):
                 _LOGGER.info("No videos found on page %s. Exiting.", page)
-                break
-        return videos+                return
+        return videos
```
```
    async def get_videos_metadata(self, since=None, camera="all", stop=10):
        """
        Fetch and return video metadata.

        :param since: Date and time to get videos from.
                      Ex: "2018/07/28 12:33:00" to retrieve videos since
                      July 28th 2018 at 12:33:00
        :param stop: Page to stop on (~25 items per page. Default page 10).
        """
        videos = []
        if since is None:
            since_epochs = self.last_refresh
        else:
            parsed_datetime = parse(since, fuzzy=True)
            since_epochs = parsed_datetime.timestamp()

        formatted_date = util.get_time(time_to_convert=since_epochs)
        _LOGGER.info("Retrieving videos since %s", formatted_date)

        for page in range(1, stop):
            response = await api.request_videos(self, time=since_epochs, page=page)
            _LOGGER.debug("Processing page %s", page)
            try:
                result = response["media"]
                if not result:
                    raise KeyError
                videos.extend(result)
            except (KeyError, TypeError):
                _LOGGER.info("No videos found on page %s. Exiting.", page)
                return
        return videos

```
