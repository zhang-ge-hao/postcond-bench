https://github.com/fronzbot/blinkpy/blob/1e868e2a19fa8b364f4e9164d1e31e7e4969c7fb/./blinkpy/sync_module.py#L746-L756
```
🈚️

async
```
```
@icontract.snapshot(lambda self, blink, file_name, max_retries: getattr(getattr(self, "prepare_download", None), "return_value", None), name="prep_ret")
@icontract.snapshot(lambda self, blink, file_name, max_retries: getattr(getattr(self, "download_video", None), "return_value", None), name="dl_ret")
@icontract.snapshot(lambda self, blink, file_name, max_retries: getattr(getattr(self, "delete_video", None), "return_value", None), name="del_ret")
@icontract.snapshot(lambda self, blink, file_name, max_retries: getattr(getattr(self, "prepare_download", None), "call_count", 0), name="prep_calls")
@icontract.snapshot(lambda self, blink, file_name, max_retries: getattr(getattr(self, "download_video", None), "call_count", 0), name="dl_calls")
@icontract.snapshot(lambda self, blink, file_name, max_retries: getattr(getattr(self, "delete_video", None), "call_count", 0), name="del_calls")
@icontract.snapshot(lambda self, blink, file_name, max_retries: getattr(getattr(self, "download_video", None), "call_args_list", []), name="dl_args")
@icontract.snapshot(lambda self, blink, file_name, max_retries: getattr(getattr(self, "delete_video", None), "call_args_list", []), name="del_args")
@icontract.ensure(lambda result, OLD: result == (bool(OLD.prep_ret) and bool(OLD.dl_ret) and bool(OLD.del_ret)))
@icontract.ensure(lambda result, OLD: (not result) or (OLD.prep_calls == 1))
@icontract.ensure(lambda result, OLD: (not result) or (OLD.dl_calls == 1))
@icontract.ensure(lambda result, OLD: (not result) or (OLD.del_calls == 1))
@icontract.ensure(lambda result, OLD: (not result) or any(((len(args) >= 2 and args[1] == file_name) or (kwargs.get("file_name") == file_name)) for args, kwargs in OLD.dl_args))
@icontract.ensure(lambda result, OLD: (not result) or all((not kwargs) or kwargs.get("max_retries", max_retries) == max_retries for args, kwargs in OLD.del_args))
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
===== 0 =====
```
         Initiate upload of media item from the sync module to
         Blink cloud servers then download to local filesystem and delete from sync.
         """
-        if await self.prepare_download(blink):
+        if await self.delete_video(blink):  # This checks for deletion instead of preparation
             if await self.download_video(blink, file_name):
                 if await self.delete_video(blink):
                     return True
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.delete_video(blink):  # This checks for deletion instead of preparation
            if await self.download_video(blink, file_name):
                if await self.delete_video(blink):
                    return True
        return False
```
===== 1 =====
```
         Initiate upload of media item from the sync module to
         Blink cloud servers then download to local filesystem and delete from sync.
         """
-        if await self.prepare_download(blink):
+        if await self.download_video(blink, "dummy_file.mp4"):  # This uses a hardcoded filename, which may not be valid
             if await self.download_video(blink, file_name):
                 if await self.delete_video(blink):
                     return True
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.download_video(blink, "dummy_file.mp4"):  # This uses a hardcoded filename, which may not be valid
            if await self.download_video(blink, file_name):
                if await self.delete_video(blink):
                    return True
        return False
```
===== 2 =====
```
         Initiate upload of media item from the sync module to
         Blink cloud servers then download to local filesystem and delete from sync.
         """
-        if await self.prepare_download(blink):
+        if await self.download_video(blink, file_name):  # This skips the preparation step entirely
             if await self.download_video(blink, file_name):
                 if await self.delete_video(blink):
                     return True
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.download_video(blink, file_name):  # This skips the preparation step entirely
            if await self.download_video(blink, file_name):
                if await self.delete_video(blink):
                    return True
        return False
```
===== 3 =====
```
         Initiate upload of media item from the sync module to
         Blink cloud servers then download to local filesystem and delete from sync.
         """
-        if await self.prepare_download(blink):
+        if not await self.prepare_download(blink):  # This inverts the condition, leading to incorrect behavior
             if await self.download_video(blink, file_name):
                 if await self.delete_video(blink):
                     return True
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if not await self.prepare_download(blink):  # This inverts the condition, leading to incorrect behavior
            if await self.download_video(blink, file_name):
                if await self.delete_video(blink):
                    return True
        return False
```
===== 4 =====
```
         Blink cloud servers then download to local filesystem and delete from sync.
         """
         if await self.prepare_download(blink):
-            if await self.download_video(blink, file_name):
+            if await self.download_video(blink, file_name) == False:
                 if await self.delete_video(blink):
                     return True
         return False
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.prepare_download(blink):
            if await self.download_video(blink, file_name) == False:
                if await self.delete_video(blink):
                    return True
        return False
```
===== 5 =====
```
         Blink cloud servers then download to local filesystem and delete from sync.
         """
         if await self.prepare_download(blink):
-            if await self.download_video(blink, file_name):
+            if await self.download_video(blink, file_name) and not await self.delete_video(blink):
                 if await self.delete_video(blink):
                     return True
         return False
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.prepare_download(blink):
            if await self.download_video(blink, file_name) and not await self.delete_video(blink):
                if await self.delete_video(blink):
                    return True
        return False
```
===== 6 =====
```
         Blink cloud servers then download to local filesystem and delete from sync.
         """
         if await self.prepare_download(blink):
-            if await self.download_video(blink, file_name):
+            if await self.download_video(blink, file_name) is None:
                 if await self.delete_video(blink):
                     return True
         return False
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.prepare_download(blink):
            if await self.download_video(blink, file_name) is None:
                if await self.delete_video(blink):
                    return True
        return False
```
===== 7 =====
```
         Blink cloud servers then download to local filesystem and delete from sync.
         """
         if await self.prepare_download(blink):
-            if await self.download_video(blink, file_name):
+            if not await self.download_video(blink, file_name):
                 if await self.delete_video(blink):
                     return True
         return False
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.prepare_download(blink):
            if not await self.download_video(blink, file_name):
                if await self.delete_video(blink):
                    return True
        return False
```
===== 8 =====
```
         """
         if await self.prepare_download(blink):
             if await self.download_video(blink, file_name):
-                if await self.delete_video(blink):
+                if await self.delete_video(blink) is False:
                     return True
         return False
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.prepare_download(blink):
            if await self.download_video(blink, file_name):
                if await self.delete_video(blink) is False:
                    return True
        return False
```
===== 9 =====
```
         """
         if await self.prepare_download(blink):
             if await self.download_video(blink, file_name):
-                if await self.delete_video(blink):
+                if await self.delete_video(blink, max_retries=5) == True:
                     return True
         return False
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.prepare_download(blink):
            if await self.download_video(blink, file_name):
                if await self.delete_video(blink, max_retries=5) == True:
                    return True
        return False
```
===== 10 =====
```
         """
         if await self.prepare_download(blink):
             if await self.download_video(blink, file_name):
-                if await self.delete_video(blink):
+                if not await self.delete_video(blink):
                     return True
         return False
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.prepare_download(blink):
            if await self.download_video(blink, file_name):
                if not await self.delete_video(blink):
                    return True
        return False
```
===== 11 =====
```
         if await self.prepare_download(blink):
             if await self.download_video(blink, file_name):
                 if await self.delete_video(blink):
-                    return True
-        return False+                    return False
+        return False
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.prepare_download(blink):
            if await self.download_video(blink, file_name):
                if await self.delete_video(blink):
                    return False
        return False

```
===== 12 =====
```
             if await self.download_video(blink, file_name):
                 if await self.delete_video(blink):
                     return True
-        return False+        return True
```
```
    async def download_video_delete(self, blink, file_name, max_retries=4) -> bool:
        """Delete local videos.

        Initiate upload of media item from the sync module to
        Blink cloud servers then download to local filesystem and delete from sync.
        """
        if await self.prepare_download(blink):
            if await self.download_video(blink, file_name):
                if await self.delete_video(blink):
                    return True
        return True

```
