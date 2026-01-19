https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/base.py#L580-L646
```
🈚️

It's hard

@icontract.snapshot(
    lambda self: copy.deepcopy(self._env_cache),
    name="cache_before",
)
@icontract.ensure(
    lambda self,
           env,
           keep,
           _KWARGS,
           result,
           OLD:
    (
        # --- 情况 1：调用前已经有缓存，必须返回之前缓存的对象 ---
        (
            f"{env}_{keep}_{_KWARGS}" in OLD.cache_before
            and result is OLD.cache_before[f"{env}_{keep}_{_KWARGS}"]
        )
        or
        # --- 情况 2：调用前没有缓存，必须按正确逻辑构造 LazySettings ---
        (
            f"{env}_{keep}_{_KWARGS}" not in OLD.cache_before
            and isinstance(result, LazySettings)
            and result._kwargs
            == normalize_kwargs(
                {
                    # 1. UPPER_DEFAULT_SETTINGS 部分
                    **{
                        key: self.get(key)
                        for key in UPPER_DEFAULT_SETTINGS
                        if key not in RENAMED_VARS
                    },
                    # 2. filter_strategy
                    **(
                        {"filter_strategy": self.filter_strategy}
                        if self.filter_strategy
                        else {}
                    ),
                    # 3. default_settings_paths 兼容逻辑
                    **(
                        {
                            "default_settings_paths": self.get(
                                "default_settings_paths"
                            )
                        }
                        if self.get("default_settings_paths")
                        else {}
                    ),
                    # 4. keep=True 时，把当前 env 的大写非 RENAMED_VARS 的值合并进去
                    **(
                        {
                            key: value
                            for key, value in self.store.to_dict()
                            .copy()
                            .items()
                            if key.isupper() and key not in RENAMED_VARS
                        }
                        if keep
                        else {}
                    ),
                    # 5. 调用方传进来的 **kwargs（这里用 _KWARGS 接住）
                    **(_KWARGS or {}),
                    # 6. 设置 FORCE_ENV_FOR_DYNACONF
                    "FORCE_ENV_FOR_DYNACONF": env,
                }
            )
            # 7. 缓存中必须已经加入当前 key 且指向 result
            and self._env_cache.get(f"{env}_{keep}_{_KWARGS}") is result
        )
    ),
    "from_env must either reuse the cached LazySettings or "
    "create a fresh LazySettings consistent with the original algorithm.",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
===== 0 =====
```
             keep {bool} -- Keep pre-existing values (default: {False})
             kwargs {dict} -- Passed directly to new instance.
         """
-        cache_key = f"{env}_{keep}_{kwargs}"
+        cache_key = None
         if cache_key in self._env_cache:
             return self._env_cache[cache_key]
 
@@ -64,4 +64,4 @@         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = None
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 1 =====
```
             kwargs {dict} -- Passed directly to new instance.
         """
         cache_key = f"{env}_{keep}_{kwargs}"
-        if cache_key in self._env_cache:
+        if cache_key in self._env_cache and self._env_cache[cache_key] is None:
             return self._env_cache[cache_key]
 
         new_data = {
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache and self._env_cache[cache_key] is None:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 2 =====
```
             kwargs {dict} -- Passed directly to new instance.
         """
         cache_key = f"{env}_{keep}_{kwargs}"
-        if cache_key in self._env_cache:
+        if cache_key in self._loaded_by_loaders:
             return self._env_cache[cache_key]
 
         new_data = {
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._loaded_by_loaders:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 3 =====
```
         new_data = {
             key: self.get(key)
             for key in UPPER_DEFAULT_SETTINGS
-            if key not in RENAMED_VARS
+            if key in RENAMED_VARS
         }
 
         if self.filter_strategy:
@@ -64,4 +64,4 @@         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 4 =====
```
             if key not in RENAMED_VARS
         }
 
-        if self.filter_strategy:
+        if not self.filter_strategy:
             # Retain the filtering strategy when switching environments
             new_data["filter_strategy"] = self.filter_strategy
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if not self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 5 =====
```
             if key not in RENAMED_VARS
         }
 
-        if self.filter_strategy:
+        if self.filter_strategy == "":
             # Retain the filtering strategy when switching environments
             new_data["filter_strategy"] = self.filter_strategy
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy == "":
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 6 =====
```
             if key not in RENAMED_VARS
         }
 
-        if self.filter_strategy:
+        if self.filter_strategy == False:
             # Retain the filtering strategy when switching environments
             new_data["filter_strategy"] = self.filter_strategy
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy == False:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 7 =====
```
             if key not in RENAMED_VARS
         }
 
-        if self.filter_strategy:
+        if self.filter_strategy is None:
             # Retain the filtering strategy when switching environments
             new_data["filter_strategy"] = self.filter_strategy
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy is None:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 8 =====
```
 
         if self.filter_strategy:
             # Retain the filtering strategy when switching environments
-            new_data["filter_strategy"] = self.filter_strategy
+            new_data["FILTER_STRATEGY"] = self.filter_strategy
 
         # This is here for backwards compatibility
         # To be removed on 4.x.x
@@ -64,4 +64,4 @@         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["FILTER_STRATEGY"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 9 =====
```
 
         if self.filter_strategy:
             # Retain the filtering strategy when switching environments
-            new_data["filter_strategy"] = self.filter_strategy
+            new_data["XXfilter_strategyXX"] = self.filter_strategy
 
         # This is here for backwards compatibility
         # To be removed on 4.x.x
@@ -64,4 +64,4 @@         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["XXfilter_strategyXX"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 10 =====
```
 
         if self.filter_strategy:
             # Retain the filtering strategy when switching environments
-            new_data["filter_strategy"] = self.filter_strategy
+            new_data["filter_strategy"] = None
 
         # This is here for backwards compatibility
         # To be removed on 4.x.x
@@ -64,4 +64,4 @@         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = None

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 11 =====
```
 
         # This is here for backwards compatibility
         # To be removed on 4.x.x
-        default_settings_paths = self.get("default_settings_paths")
+        default_settings_paths = self.get("default_settings_paths", default="fallback_value")
         if default_settings_paths:  # pragma: no cover
             new_data["default_settings_paths"] = default_settings_paths
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths", default="fallback_value")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 12 =====
```
         # This is here for backwards compatibility
         # To be removed on 4.x.x
         default_settings_paths = self.get("default_settings_paths")
-        if default_settings_paths:  # pragma: no cover
+        if default_settings_paths is None:  # pragma: no cover
             new_data["default_settings_paths"] = default_settings_paths
 
         if keep:
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths is None:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 13 =====
```
         # This is here for backwards compatibility
         # To be removed on 4.x.x
         default_settings_paths = self.get("default_settings_paths")
-        if default_settings_paths:  # pragma: no cover
+        if not default_settings_paths:  # pragma: no cover
             new_data["default_settings_paths"] = default_settings_paths
 
         if keep:
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if not default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 14 =====
```
         if default_settings_paths:  # pragma: no cover
             new_data["default_settings_paths"] = default_settings_paths
 
-        if keep:
+        if keep and False:
             # keep existing values from current env
             new_data.update(
                 {
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep and False:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 15 =====
```
         if default_settings_paths:  # pragma: no cover
             new_data["default_settings_paths"] = default_settings_paths
 
-        if keep:
+        if keep is None:
             # keep existing values from current env
             new_data.update(
                 {
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep is None:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 16 =====
```
         if default_settings_paths:  # pragma: no cover
             new_data["default_settings_paths"] = default_settings_paths
 
-        if keep:
+        if keep or True:
             # keep existing values from current env
             new_data.update(
                 {
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep or True:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 17 =====
```
         if default_settings_paths:  # pragma: no cover
             new_data["default_settings_paths"] = default_settings_paths
 
-        if keep:
+        if not keep:
             # keep existing values from current env
             new_data.update(
                 {
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if not keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 18 =====
```
                 {
                     key: value
                     for key, value in self.store.to_dict().copy().items()
-                    if key.isupper() and key not in RENAMED_VARS
+                    if key.isupper() and key in RENAMED_VARS
                 }
             )
 
@@ -64,4 +64,4 @@         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 19 =====
```
                 {
                     key: value
                     for key, value in self.store.to_dict().copy().items()
-                    if key.isupper() and key not in RENAMED_VARS
+                    if key.isupper() or key not in RENAMED_VARS
                 }
             )
 
@@ -64,4 +64,4 @@         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() or key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 20 =====
```
                 }
             )
 
-        new_data.update(kwargs)
+        new_data.update({k: v for k, v in kwargs.items() if k in ['key1', 'key2']})
         new_data["FORCE_ENV_FOR_DYNACONF"] = env
         new_settings = LazySettings(**new_data)
         self._env_cache[cache_key] = new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update({k: v for k, v in kwargs.items() if k in ['key1', 'key2']})
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 21 =====
```
                 }
             )
 
-        new_data.update(kwargs)
+        new_data.update({k: v for k, v in kwargs.items() if k not in new_data})
         new_data["FORCE_ENV_FOR_DYNACONF"] = env
         new_settings = LazySettings(**new_data)
         self._env_cache[cache_key] = new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update({k: v for k, v in kwargs.items() if k not in new_data})
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 22 =====
```
                 }
             )
 
-        new_data.update(kwargs)
+        new_data.update({k: v for k, v in kwargs.items() if k.startswith('invalid_')})
         new_data["FORCE_ENV_FOR_DYNACONF"] = env
         new_settings = LazySettings(**new_data)
         self._env_cache[cache_key] = new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update({k: v for k, v in kwargs.items() if k.startswith('invalid_')})
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 23 =====
```
                 }
             )
 
-        new_data.update(kwargs)
+        new_data.update({k: v for k, v in kwargs.items() if v is None})
         new_data["FORCE_ENV_FOR_DYNACONF"] = env
         new_settings = LazySettings(**new_data)
         self._env_cache[cache_key] = new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update({k: v for k, v in kwargs.items() if v is None})
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 24 =====
```
             )
 
         new_data.update(kwargs)
-        new_data["FORCE_ENV_FOR_DYNACONF"] = env
+        new_data["FORCE_ENV_FOR_DYNACONF"] = None
         new_settings = LazySettings(**new_data)
         self._env_cache[cache_key] = new_settings
 
         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = None
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 25 =====
```
             )
 
         new_data.update(kwargs)
-        new_data["FORCE_ENV_FOR_DYNACONF"] = env
+        new_data["XXFORCE_ENV_FOR_DYNACONFXX"] = env
         new_settings = LazySettings(**new_data)
         self._env_cache[cache_key] = new_settings
 
         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["XXFORCE_ENV_FOR_DYNACONFXX"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 26 =====
```
 
         new_data.update(kwargs)
         new_data["FORCE_ENV_FOR_DYNACONF"] = env
-        new_settings = LazySettings(**new_data)
+        new_settings = LazySettings(**new_data, _kwargs={})
         self._env_cache[cache_key] = new_settings
 
         # update source metadata for inspecting
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data, _kwargs={})
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 27 =====
```
 
         new_data.update(kwargs)
         new_data["FORCE_ENV_FOR_DYNACONF"] = env
-        new_settings = LazySettings(**new_data)
+        new_settings = LazySettings(**new_data, extra_param=True)
         self._env_cache[cache_key] = new_settings
 
         # update source metadata for inspecting
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data, extra_param=True)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings
```
===== 28 =====
```
         new_data.update(kwargs)
         new_data["FORCE_ENV_FOR_DYNACONF"] = env
         new_settings = LazySettings(**new_data)
-        self._env_cache[cache_key] = new_settings
+        self._env_cache[cache_key] = None
 
         # update source metadata for inspecting
         self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
 
-        return new_settings+        return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = None

        # update source metadata for inspecting
        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)

        return new_settings

```
===== 29 =====
```
         self._env_cache[cache_key] = new_settings
 
         # update source metadata for inspecting
-        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
+        self._loaded_by_loaders = new_settings._loaded_by_loaders  # This overwrites the existing loaders instead of merging.
 
         return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders = new_settings._loaded_by_loaders  # This overwrites the existing loaders instead of merging.

        return new_settings
```
===== 30 =====
```
         self._env_cache[cache_key] = new_settings
 
         # update source metadata for inspecting
-        self._loaded_by_loaders.update(new_settings._loaded_by_loaders)
+        self._loaded_by_loaders.update({})  # This effectively clears the existing loaders by updating with an empty dictionary.
 
         return new_settings
```
```
    def from_env(self, env="", keep=False, **kwargs):
        """Return a new isolated settings object pointing to specified env.

        Example of settings.toml::

            [development]
            message = 'This is in dev'
            [other]
            message = 'this is in other env'

        Program::

            >>> from dynaconf import settings
            >>> print(settings.MESSAGE)
            'This is in dev'
            >>> print(settings.from_env('other').MESSAGE)
            'This is in other env'
            # The existing settings object remains the same.
            >>> print(settings.MESSAGE)
            'This is in dev'

        Arguments:
            env {str} -- Env to load (development, production, custom)

        Keyword Arguments:
            keep {bool} -- Keep pre-existing values (default: {False})
            kwargs {dict} -- Passed directly to new instance.
        """
        cache_key = f"{env}_{keep}_{kwargs}"
        if cache_key in self._env_cache:
            return self._env_cache[cache_key]

        new_data = {
            key: self.get(key)
            for key in UPPER_DEFAULT_SETTINGS
            if key not in RENAMED_VARS
        }

        if self.filter_strategy:
            # Retain the filtering strategy when switching environments
            new_data["filter_strategy"] = self.filter_strategy

        # This is here for backwards compatibility
        # To be removed on 4.x.x
        default_settings_paths = self.get("default_settings_paths")
        if default_settings_paths:  # pragma: no cover
            new_data["default_settings_paths"] = default_settings_paths

        if keep:
            # keep existing values from current env
            new_data.update(
                {
                    key: value
                    for key, value in self.store.to_dict().copy().items()
                    if key.isupper() and key not in RENAMED_VARS
                }
            )

        new_data.update(kwargs)
        new_data["FORCE_ENV_FOR_DYNACONF"] = env
        new_settings = LazySettings(**new_data)
        self._env_cache[cache_key] = new_settings

        # update source metadata for inspecting
        self._loaded_by_loaders.update({})  # This effectively clears the existing loaders by updating with an empty dictionary.

        return new_settings
```
