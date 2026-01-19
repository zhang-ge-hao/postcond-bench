https://github.com/SolaceLabs/solace-agent-mesh/blob/6564748e81c0625394b55124c4d80e4af2f6042b/./src/solace_agent_mesh/agent/adk/models/lite_llm.py#L689-L733
```
🈚️

E   ModuleNotFoundError: No module named 'icontract'

@icontract.ensure(
    # 1. cache_strategy 规范化逻辑：
    #    - 如果传入的是合法值，就原样保留；
    #    - 如果传入的是非法值，就必须归一化为 "5m"。
    lambda self, cache_strategy:
    (
        cache_strategy in {"none", "5m", "1h"}
        and self._cache_strategy == cache_strategy
    )
    or
    (
        cache_strategy not in {"none", "5m", "1h"}
        and self._cache_strategy == "5m"
    )
)
@icontract.ensure(
    # 2. _additional_args 里不允许再出现这些内部保留参数：
    #    它们必须在 __init__ 里被 pop 掉。
    lambda self:
    all(
        key not in self._additional_args
        for key in ("llm_client", "messages", "tools", "stream")
    )
)
@icontract.ensure(
    # 3. 如果创建了 OAuth token manager，那么类型必须正确；
    #    如果没创建，则必须为 None。
    lambda self:
    (
        self._oauth_token_manager is None
        or isinstance(
            self._oauth_token_manager,
            OAuth2ClientCredentialsTokenManager,
        )
    )
)
@icontract.ensure(
    # 4. 原始 kwargs 中是否提供完整 OAuth 配置
    #    必须和 _oauth_token_manager 是否存在保持“等价”。
    #
    #   - 如果一开始就给了 token_url + client_id + client_secret，
    #     那么初始化之后必须有 _oauth_token_manager（且不为 None）。
    #   - 如果这三者不全，则初始化之后必须没有 _oauth_token_manager（为 None）。
    #
    # 注意：这里用的是 OLD.kwargs，拿到的是进入 __init__ 之前的原始 **kwargs，
    #       和 self._additional_args / kwargs 目前的内容无关。
    lambda self, kwargs, OLD:
    (
        {"oauth_token_url", "oauth_client_id", "oauth_client_secret"}.issubset(
            set(OLD.kwargs.keys())
        )
    )
    == (self._oauth_token_manager is not None)
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
===== 0 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["LITELLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LITELLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 1 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["LiteLLM", "LITELLM PROXY", "LiteLLM Router", "litellm"]:
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LITELLM PROXY", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 2 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LITELLM ROUTER", "litellm"]:
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LITELLM ROUTER", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 3 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["LiteLLM", "LiteLLM Proxy", "XXLiteLLM RouterXX", "litellm"]:
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "XXLiteLLM RouterXX", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 4 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["LiteLLM", "LiteLLM Proxy", "litellm router", "litellm"]:
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "litellm router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 5 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["LiteLLM", "LiteLLM Proxy", "litellm"]:  # Missing "LiteLLM Router"
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "litellm"]:  # Missing "LiteLLM Router"
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 6 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["LiteLLM", "XXLiteLLM ProxyXX", "LiteLLM Router", "litellm"]:
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "XXLiteLLM ProxyXX", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 7 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["LiteLLM", "litellm proxy", "LiteLLM Router", "litellm"]:
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "litellm proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 8 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["XXLiteLLMXX", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["XXLiteLLMXX", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 9 =====
```
 
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
-        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
+        for logger_name in ["litellm", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["litellm", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 10 =====
```
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
         for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
-            logging.getLogger(logger_name).handlers.clear()
+            logging.getLogger(None).handlers.clear()
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(None).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 11 =====
```
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
         for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
-            logging.getLogger(logger_name).handlers.clear()
+            logging.getLogger(logger_name).addHandler(logging.StreamHandler())
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).addHandler(logging.StreamHandler())

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 12 =====
```
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
         for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
-            logging.getLogger(logger_name).handlers.clear()
+            logging.getLogger(logger_name).handlers = [logging.FileHandler('logfile.log')]
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers = [logging.FileHandler('logfile.log')]

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 13 =====
```
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
         for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
-            logging.getLogger(logger_name).handlers.clear()
+            logging.getLogger(logger_name).handlers.append(logging.NullHandler())
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.append(logging.NullHandler())

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 14 =====
```
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
         for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
-            logging.getLogger(logger_name).handlers.clear()
+            logging.getLogger(logger_name).propagate = False
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).propagate = False

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 15 =====
```
         # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
         # Logging is an application concern and libraries should not set handlers/formatters.
         for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
-            logging.getLogger(logger_name).handlers.clear()
+            logging.getLogger(logger_name).setLevel(logging.DEBUG)
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).setLevel(logging.DEBUG)

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 16 =====
```
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
-        valid_strategies = ["none", "5m", "1h"]
+        valid_strategies = ["NONE", "5m", "1h"]
         if cache_strategy not in valid_strategies:
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["NONE", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 17 =====
```
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
-        valid_strategies = ["none", "5m", "1h"]
+        valid_strategies = ["XXnoneXX", "5m", "1h"]
         if cache_strategy not in valid_strategies:
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["XXnoneXX", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 18 =====
```
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
-        valid_strategies = ["none", "5m", "1h"]
+        valid_strategies = ["none", "5m", "1H"]
         if cache_strategy not in valid_strategies:
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1H"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 19 =====
```
             logging.getLogger(logger_name).handlers.clear()
 
         # Validate and store cache strategy
-        valid_strategies = ["none", "5m", "1h"]
+        valid_strategies = ["none", "5m", "XX1hXX"]
         if cache_strategy not in valid_strategies:
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "XX1hXX"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 20 =====
```
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
-        if cache_strategy not in valid_strategies:
+        if cache_strategy == "5m" and cache_strategy == "1h":
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                 cache_strategy,
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy == "5m" and cache_strategy == "1h":
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 21 =====
```
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
-        if cache_strategy not in valid_strategies:
+        if cache_strategy == "5m" or cache_strategy == "1h":
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                 cache_strategy,
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy == "5m" or cache_strategy == "1h":
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 22 =====
```
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
-        if cache_strategy not in valid_strategies:
+        if cache_strategy == "none":
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                 cache_strategy,
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy == "none":
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 23 =====
```
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
-        if cache_strategy not in valid_strategies:
+        if cache_strategy in valid_strategies:
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                 cache_strategy,
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 24 =====
```
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
-        if cache_strategy not in valid_strategies:
+        if cache_strategy in valid_strategies:
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                 cache_strategy,
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 25 =====
```
 
         # Validate and store cache strategy
         valid_strategies = ["none", "5m", "1h"]
-        if cache_strategy not in valid_strategies:
+        if cache_strategy not in ["5m", "1h", "invalid_option"]:
             logger.warning(
                 "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                 cache_strategy,
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in ["5m", "1h", "invalid_option"]:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 26 =====
```
         valid_strategies = ["none", "5m", "1h"]
         if cache_strategy not in valid_strategies:
             logger.warning(
-                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
+                "INVALID CACHE_STRATEGY '%S'. VALID OPTIONS ARE: %S. DEFAULTING TO '5M'.",
                 cache_strategy,
                 valid_strategies,
             )
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "INVALID CACHE_STRATEGY '%S'. VALID OPTIONS ARE: %S. DEFAULTING TO '5M'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 27 =====
```
         valid_strategies = ["none", "5m", "1h"]
         if cache_strategy not in valid_strategies:
             logger.warning(
-                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
+                "invalid cache_strategy '%s'. valid options are: %s. defaulting to '5m'.",
                 cache_strategy,
                 valid_strategies,
             )
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "invalid cache_strategy '%s'. valid options are: %s. defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 28 =====
```
         valid_strategies = ["none", "5m", "1h"]
         if cache_strategy not in valid_strategies:
             logger.warning(
-                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
+                None,
                 cache_strategy,
                 valid_strategies,
             )
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                None,
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 29 =====
```
         valid_strategies = ["none", "5m", "1h"]
         if cache_strategy not in valid_strategies:
             logger.warning(
-                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                 cache_strategy,
                 valid_strategies,
             )
@@ -42,4 +41,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 30 =====
```
                 cache_strategy,
                 valid_strategies,
             )
-            cache_strategy = "5m"
+            cache_strategy = "5M"
         self._cache_strategy = cache_strategy
         logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
 
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5M"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 31 =====
```
                 cache_strategy,
                 valid_strategies,
             )
-            cache_strategy = "5m"
+            cache_strategy = "XX5mXX"
         self._cache_strategy = cache_strategy
         logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
 
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "XX5mXX"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 32 =====
```
                 cache_strategy,
                 valid_strategies,
             )
-            cache_strategy = "5m"
+            cache_strategy = None
         self._cache_strategy = cache_strategy
         logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
 
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = None
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 33 =====
```
                 valid_strategies,
             )
             cache_strategy = "5m"
-        self._cache_strategy = cache_strategy
+        self._cache_strategy = None
         logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
 
         # Extract OAuth configuration if present
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = None
        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 34 =====
```
             )
             cache_strategy = "5m"
         self._cache_strategy = cache_strategy
-        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
+        logger.debug("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
 
         # Extract OAuth configuration if present
         oauth_config = self._extract_oauth_config(self._additional_args)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.debug("LiteLlm initialized with cache strategy: %s", self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 35 =====
```
             )
             cache_strategy = "5m"
         self._cache_strategy = cache_strategy
-        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
+        logger.info("LiteLlm initialized with cache strategy: %s", )
 
         # Extract OAuth configuration if present
         oauth_config = self._extract_oauth_config(self._additional_args)
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", )

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 36 =====
```
             )
             cache_strategy = "5m"
         self._cache_strategy = cache_strategy
-        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
+        logger.info("LiteLlm initialized with cache strategy: %s", None)
 
         # Extract OAuth configuration if present
         oauth_config = self._extract_oauth_config(self._additional_args)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", None)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 37 =====
```
             )
             cache_strategy = "5m"
         self._cache_strategy = cache_strategy
-        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
+        logger.info("LiteLlm initialized with cache strategy: %s", None)
 
         # Extract OAuth configuration if present
         oauth_config = self._extract_oauth_config(self._additional_args)
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized with cache strategy: %s", None)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 38 =====
```
             )
             cache_strategy = "5m"
         self._cache_strategy = cache_strategy
-        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
+        logger.info("LiteLlm initialized without cache strategy.")
 
         # Extract OAuth configuration if present
         oauth_config = self._extract_oauth_config(self._additional_args)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info("LiteLlm initialized without cache strategy.")

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
===== 39 =====
```
             )
             cache_strategy = "5m"
         self._cache_strategy = cache_strategy
-        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
+        logger.info(None, self._cache_strategy)
 
         # Extract OAuth configuration if present
         oauth_config = self._extract_oauth_config(self._additional_args)
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info(None, self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 40 =====
```
             )
             cache_strategy = "5m"
         self._cache_strategy = cache_strategy
-        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
+        logger.info(self._cache_strategy)
 
         # Extract OAuth configuration if present
         oauth_config = self._extract_oauth_config(self._additional_args)
@@ -42,4 +42,4 @@         self._additional_args.pop("messages", None)
         self._additional_args.pop("tools", None)
         # public api called from runner determines to stream or not
-        self._additional_args.pop("stream", None)+        self._additional_args.pop("stream", None)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.info(self._cache_strategy)

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

```
===== 41 =====
```
             )
             cache_strategy = "5m"
         self._cache_strategy = cache_strategy
-        logger.info("LiteLlm initialized with cache strategy: %s", self._cache_strategy)
+        logger.warning("LiteLlm initialized with cache strategy: %s", "default")
 
         # Extract OAuth configuration if present
         oauth_config = self._extract_oauth_config(self._additional_args)
```
```
    def __init__(self, model: str, cache_strategy: str = "5m", **kwargs):
        """Initializes the LiteLlm class.

        Args:
          model: The name of the LiteLlm model.
          cache_strategy: Cache strategy to use. Options: "none", "5m" (ephemeral), "1h" (extended).
                         Defaults to "5m" for backward compatibility.
          **kwargs: Additional arguments to pass to the litellm completion api.
                   Can include OAuth configuration parameters.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs.copy()

        # Remove handlers added by LiteLLM as they produce duplicate and misformatted logs.
        # Logging is an application concern and libraries should not set handlers/formatters.
        for logger_name in ["LiteLLM", "LiteLLM Proxy", "LiteLLM Router", "litellm"]:
            logging.getLogger(logger_name).handlers.clear()

        # Validate and store cache strategy
        valid_strategies = ["none", "5m", "1h"]
        if cache_strategy not in valid_strategies:
            logger.warning(
                "Invalid cache_strategy '%s'. Valid options are: %s. Defaulting to '5m'.",
                cache_strategy,
                valid_strategies,
            )
            cache_strategy = "5m"
        self._cache_strategy = cache_strategy
        logger.warning("LiteLlm initialized with cache strategy: %s", "default")

        # Extract OAuth configuration if present
        oauth_config = self._extract_oauth_config(self._additional_args)
        if oauth_config:
            self._oauth_token_manager = OAuth2ClientCredentialsTokenManager(**oauth_config)
            logger.info("OAuth2 token manager initialized for model: %s", model)
        else:
            self._oauth_token_manager = None

        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)
```
