https://github.com/vndee/llm-sandbox/blob/218b9d3d8523bac44e60e241ab72f7e160f8ad30/./llm_sandbox/kubernetes.py#L302-L390
```
🈚️
Timeout

@icontract.snapshot(lambda client: client, name="snap_client")
@icontract.snapshot(lambda pod_manifest: pod_manifest, name="snap_pod_manifest")
@icontract.ensure(
    lambda self,
            client,
            image,
            lang,
            verbose,
            kube_namespace,
            env_vars,
            pod_manifest,
            workdir,
            security_policy,
            default_timeout,
            execution_timeout,
            session_timeout,
            container_id,
            skip_environment_setup,
            OLD:
    self.config.image == image
    and self.client is not None
    and self.config.lang == SupportedLanguage(lang.upper())
    and self.config.verbose == verbose
    and self.config.workdir == workdir
    and self.config.security_policy == security_policy
    and self.config.default_timeout == default_timeout
    and self.config.execution_timeout == execution_timeout
    and self.config.session_timeout == session_timeout
    and self.config.container_id == container_id
    and self.config.skip_environment_setup == skip_environment_setup
    and self.verbose == verbose
    and self.container is None
    and self.is_open is False
    and self._session_start_time is None
    and self._session_timer is None
    and self.using_existing_container == self.config.is_using_existing_container()
    and self.language_handler is not None
    and (
        self.kube_namespace
        == (
            OLD.snap_pod_manifest.get("metadata", {}).get("namespace", kube_namespace)
            if (
                not self.using_existing_container
                and isinstance(OLD.snap_pod_manifest, dict)
                and isinstance(OLD.snap_pod_manifest.get("metadata", {}), dict)
            )
            else kube_namespace
        )
    )
    and self.stream is False
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74]
===== 0 =====
```
 
         """
         config = SessionConfig(
-            image=image,
+            image="",  # Setting image to an empty string
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image="",  # Setting image to an empty string
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 1 =====
```
 
         """
         config = SessionConfig(
-            image=image,
+            image="invalid_image_name",
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image="invalid_image_name",
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 2 =====
```
 
         """
         config = SessionConfig(
-            image=image,
+            image=DefaultImage.__dict__.get(lang.upper(), "default_image"),
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=DefaultImage.__dict__.get(lang.upper(), "default_image"),
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 3 =====
```
 
         """
         config = SessionConfig(
-            image=image,
+            image=None,
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=None,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 4 =====
```
 
         """
         config = SessionConfig(
-            image=image,
+            image=None,
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=None,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 5 =====
```
 
         """
         config = SessionConfig(
-            image=image,
+            image=lang,  # Incorrectly using lang instead of the image
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=lang,  # Incorrectly using lang instead of the image
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 6 =====
```
 
         """
         config = SessionConfig(
-            image=image,
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
@@ -86,4 +85,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 7 =====
```
         """
         config = SessionConfig(
             image=image,
-            lang=SupportedLanguage(lang.upper()),
+            lang=SupportedLanguage("PYTHON"),  # Hardcodes the language to Python regardless of input
             verbose=verbose,
             workdir=workdir,
             security_policy=security_policy,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage("PYTHON"),  # Hardcodes the language to Python regardless of input
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 8 =====
```
         """
         config = SessionConfig(
             image=image,
-            lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
             security_policy=security_policy,
@@ -86,4 +85,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 9 =====
```
         config = SessionConfig(
             image=image,
             lang=SupportedLanguage(lang.upper()),
-            verbose=verbose,
+            verbose=0,
             workdir=workdir,
             security_policy=security_policy,
             default_timeout=default_timeout,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=0,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 10 =====
```
         config = SessionConfig(
             image=image,
             lang=SupportedLanguage(lang.upper()),
-            verbose=verbose,
+            verbose=False,
             workdir=workdir,
             security_policy=security_policy,
             default_timeout=default_timeout,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=False,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 11 =====
```
         config = SessionConfig(
             image=image,
             lang=SupportedLanguage(lang.upper()),
-            verbose=verbose,
+            verbose=True,
             workdir=workdir,
             security_policy=security_policy,
             default_timeout=default_timeout,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=True,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 12 =====
```
         config = SessionConfig(
             image=image,
             lang=SupportedLanguage(lang.upper()),
-            verbose=verbose,
             workdir=workdir,
             security_policy=security_policy,
             default_timeout=default_timeout,
@@ -86,4 +85,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 13 =====
```
             image=image,
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
-            workdir=workdir,
+            env_vars=env_vars,  # Incorrectly assigns env_vars instead of workdir
             security_policy=security_policy,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            env_vars=env_vars,  # Incorrectly assigns env_vars instead of workdir
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 14 =====
```
             image=image,
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
-            workdir=workdir,
+            kube_namespace=kube_namespace,  # Incorrectly assigns kube_namespace instead of workdir
             security_policy=security_policy,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            kube_namespace=kube_namespace,  # Incorrectly assigns kube_namespace instead of workdir
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 15 =====
```
             image=image,
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
-            workdir=workdir,
             security_policy=security_policy,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
@@ -86,4 +85,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 16 =====
```
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
-            security_policy=security_policy,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
             session_timeout=session_timeout,
@@ -86,4 +85,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 17 =====
```
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
-            security_policy=security_policy,
+            security_policy=None,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
             session_timeout=session_timeout,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=None,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 18 =====
```
             lang=SupportedLanguage(lang.upper()),
             verbose=verbose,
             workdir=workdir,
-            security_policy=security_policy,
+            security_policy=None,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
             session_timeout=session_timeout,
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=None,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 19 =====
```
             verbose=verbose,
             workdir=workdir,
             security_policy=security_policy,
-            default_timeout=default_timeout,
+            default_timeout=0,  # This sets the timeout to zero, which may cause immediate timeouts
             execution_timeout=execution_timeout,
             session_timeout=session_timeout,
             container_id=container_id,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=0,  # This sets the timeout to zero, which may cause immediate timeouts
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 20 =====
```
             verbose=verbose,
             workdir=workdir,
             security_policy=security_policy,
-            default_timeout=default_timeout,
+            default_timeout=None,
             execution_timeout=execution_timeout,
             session_timeout=session_timeout,
             container_id=container_id,
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=None,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 21 =====
```
             verbose=verbose,
             workdir=workdir,
             security_policy=security_policy,
-            default_timeout=default_timeout,
+            default_timeout=None,  # This will ignore the provided default_timeout value
             execution_timeout=execution_timeout,
             session_timeout=session_timeout,
             container_id=container_id,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=None,  # This will ignore the provided default_timeout value
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 22 =====
```
             workdir=workdir,
             security_policy=security_policy,
             default_timeout=default_timeout,
-            execution_timeout=execution_timeout,
+            execution_timeout=0,
             session_timeout=session_timeout,
             container_id=container_id,
             skip_environment_setup=skip_environment_setup,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=0,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 23 =====
```
             workdir=workdir,
             security_policy=security_policy,
             default_timeout=default_timeout,
-            execution_timeout=execution_timeout,
+            execution_timeout=None,
             session_timeout=session_timeout,
             container_id=container_id,
             skip_environment_setup=skip_environment_setup,
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=None,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 24 =====
```
             workdir=workdir,
             security_policy=security_policy,
             default_timeout=default_timeout,
-            execution_timeout=execution_timeout,
+            execution_timeout=None,
             session_timeout=session_timeout,
             container_id=container_id,
             skip_environment_setup=skip_environment_setup,
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=None,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 25 =====
```
             workdir=workdir,
             security_policy=security_policy,
             default_timeout=default_timeout,
-            execution_timeout=execution_timeout,
             session_timeout=session_timeout,
             container_id=container_id,
             skip_environment_setup=skip_environment_setup,
@@ -86,4 +85,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 26 =====
```
             security_policy=security_policy,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
-            session_timeout=session_timeout,
             container_id=container_id,
             skip_environment_setup=skip_environment_setup,
         )
@@ -86,4 +85,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 27 =====
```
             security_policy=security_policy,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
-            session_timeout=session_timeout,
+            session_timeout=None,
             container_id=container_id,
             skip_environment_setup=skip_environment_setup,
         )
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=None,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 28 =====
```
             security_policy=security_policy,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
-            session_timeout=session_timeout,
+            session_timeout=None,
             container_id=container_id,
             skip_environment_setup=skip_environment_setup,
         )
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=None,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 29 =====
```
             security_policy=security_policy,
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
-            session_timeout=session_timeout,
+            session_timeout=default_timeout,
             container_id=container_id,
             skip_environment_setup=skip_environment_setup,
         )
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=default_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 30 =====
```
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
             session_timeout=session_timeout,
-            container_id=container_id,
+            container_id="",
             skip_environment_setup=skip_environment_setup,
         )
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id="",
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 31 =====
```
             default_timeout=default_timeout,
             execution_timeout=execution_timeout,
             session_timeout=session_timeout,
-            container_id=container_id,
+            container_id=uuid.uuid4().hex,
             skip_environment_setup=skip_environment_setup,
         )
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=uuid.uuid4().hex,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 32 =====
```
 
         super().__init__(config=config, **kwargs)
 
-        if not client:
+        if client == "":
             self._log("Using local Kubernetes context since client is not provided.")
             from kubernetes import config as k8s_config
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if client == "":
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 33 =====
```
 
         super().__init__(config=config, **kwargs)
 
-        if not client:
+        if client == "default":
             self._log("Using local Kubernetes context since client is not provided.")
             from kubernetes import config as k8s_config
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if client == "default":
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 34 =====
```
             from kubernetes import config as k8s_config
 
             k8s_config.load_kube_config()
-            self.client = CoreV1Api()
+            self.client = None
         else:
             self.client = client
 
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = None
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 35 =====
```
             from kubernetes import config as k8s_config
 
             k8s_config.load_kube_config()
-            self.client = CoreV1Api()
+            self.client = None  # Assigning None instead of a valid client
         else:
             self.client = client
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = None  # Assigning None instead of a valid client
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 36 =====
```
             k8s_config.load_kube_config()
             self.client = CoreV1Api()
         else:
-            self.client = client
+            self.client = None
 
         self.kube_namespace = kube_namespace
         self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = None

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 37 =====
```
         else:
             self.client = client
 
-        self.kube_namespace = kube_namespace
+        self.kube_namespace = None
         self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
 
         # Generate unique pod name (only if not using existing pod)
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = None
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 38 =====
```
             self.client = client
 
         self.kube_namespace = kube_namespace
-        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
+        self.container_api = KubernetesContainerAPI(None, kube_namespace)
 
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(None, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 39 =====
```
             self.client = client
 
         self.kube_namespace = kube_namespace
-        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
+        self.container_api = KubernetesContainerAPI(kube_namespace)
 
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 40 =====
```
             self.client = client
 
         self.kube_namespace = kube_namespace
-        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
+        self.container_api = KubernetesContainerAPI(self.client, )
 
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, )

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 41 =====
```
             self.client = client
 
         self.kube_namespace = kube_namespace
-        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
+        self.container_api = KubernetesContainerAPI(self.client, None)
 
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, None)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 42 =====
```
             self.client = client
 
         self.kube_namespace = kube_namespace
-        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
+        self.container_api = KubernetesContainerAPI(self.client, namespace="default")
 
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, namespace="default")

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 43 =====
```
             self.client = client
 
         self.kube_namespace = kube_namespace
-        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
+        self.container_api = KubernetesContainerAPI(self.client, namespace=None)
 
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, namespace=None)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 44 =====
```
             self.client = client
 
         self.kube_namespace = kube_namespace
-        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
+        self.container_api = None
 
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = None

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 45 =====
```
         self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
 
         # Generate unique pod name (only if not using existing pod)
-        if not self.using_existing_container:
+        if self.kube_namespace == "default":  # Incorrectly checks for the default namespace
             short_uuid = uuid.uuid4().hex[:8]
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if self.kube_namespace == "default":  # Incorrectly checks for the default namespace
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 46 =====
```
         self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
 
         # Generate unique pod name (only if not using existing pod)
-        if not self.using_existing_container:
+        if self.using_existing_container:
             short_uuid = uuid.uuid4().hex[:8]
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 47 =====
```
         self.container_api = KubernetesContainerAPI(self.client, kube_namespace)
 
         # Generate unique pod name (only if not using existing pod)
-        if not self.using_existing_container:
+        if self.using_existing_container:  # Incorrectly checks for existing container
             short_uuid = uuid.uuid4().hex[:8]
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if self.using_existing_container:  # Incorrectly checks for existing container
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 48 =====
```
 
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
-            short_uuid = uuid.uuid4().hex[:8]
+            short_uuid = None
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = None
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 49 =====
```
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
             short_uuid = uuid.uuid4().hex[:8]
-            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
+            self.pod_name = None
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
             self._reconfigure_with_pod_manifest()
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = None
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 50 =====
```
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
             short_uuid = uuid.uuid4().hex[:8]
-            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
+            self.pod_name = f"sandbox-{lang.upper()}-{short_uuid}"
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
             self._reconfigure_with_pod_manifest()
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.upper()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 51 =====
```
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
             short_uuid = uuid.uuid4().hex[:8]
-            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
+            self.pod_name = f"sandbox-{lang.upper()}-{short_uuid}"  # Incorrectly uses upper case for language
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
             self._reconfigure_with_pod_manifest()
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.upper()}-{short_uuid}"  # Incorrectly uses upper case for language
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 52 =====
```
         # Generate unique pod name (only if not using existing pod)
         if not self.using_existing_container:
             short_uuid = uuid.uuid4().hex[:8]
-            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
+            self.pod_name = f"sandbox-{short_uuid}"  # Omits the language entirely
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
             self._reconfigure_with_pod_manifest()
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{short_uuid}"  # Omits the language entirely
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 53 =====
```
         if not self.using_existing_container:
             short_uuid = uuid.uuid4().hex[:8]
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
-            self.env_vars = env_vars
+            self.env_vars = None
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
             self._reconfigure_with_pod_manifest()
 
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = None
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 54 =====
```
             short_uuid = uuid.uuid4().hex[:8]
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
-            self.pod_manifest = pod_manifest or self._default_pod_manifest()
+            self.pod_manifest = pod_manifest or self._default_pod_manifest() if verbose else self._default_pod_manifest()  # Ignoring the provided manifest if verbose is False
             self._reconfigure_with_pod_manifest()
 
             # Extract container name from pod manifest for command execution
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest() if verbose else self._default_pod_manifest()  # Ignoring the provided manifest if verbose is False
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 55 =====
```
             short_uuid = uuid.uuid4().hex[:8]
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
-            self.pod_manifest = pod_manifest or self._default_pod_manifest()
+            self.pod_manifest = self._default_pod_manifest()  # Always using the default manifest, ignoring provided one
             self._reconfigure_with_pod_manifest()
 
             # Extract container name from pod manifest for command execution
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = self._default_pod_manifest()  # Always using the default manifest, ignoring provided one
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 56 =====
```
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
-            self._reconfigure_with_pod_manifest()
+            self.container_name = "sandbox-container"  # Overwriting the container name to a static value
 
             # Extract container name from pod manifest for command execution
             containers = self.pod_manifest.get("spec", {}).get("containers", [])
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self.container_name = "sandbox-container"  # Overwriting the container name to a static value

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 57 =====
```
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
-            self._reconfigure_with_pod_manifest()
+            self.env_vars = None  # Setting environment variables to None, which may lead to missing configurations
 
             # Extract container name from pod manifest for command execution
             containers = self.pod_manifest.get("spec", {}).get("containers", [])
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self.env_vars = None  # Setting environment variables to None, which may lead to missing configurations

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 58 =====
```
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
-            self._reconfigure_with_pod_manifest()
+            self.kube_namespace = "default"  # Hardcoding the namespace to "default" regardless of the provided value
 
             # Extract container name from pod manifest for command execution
             containers = self.pod_manifest.get("spec", {}).get("containers", [])
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self.kube_namespace = "default"  # Hardcoding the namespace to "default" regardless of the provided value

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 59 =====
```
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
-            self._reconfigure_with_pod_manifest()
+            self.pod_manifest = {}  # Resetting the pod manifest to an empty dictionary
 
             # Extract container name from pod manifest for command execution
             containers = self.pod_manifest.get("spec", {}).get("containers", [])
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self.pod_manifest = {}  # Resetting the pod manifest to an empty dictionary

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 60 =====
```
             self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
             self.env_vars = env_vars
             self.pod_manifest = pod_manifest or self._default_pod_manifest()
-            self._reconfigure_with_pod_manifest()
+            self.pod_name = "sandbox-default"  # Changing the pod name to a static value, losing uniqueness
 
             # Extract container name from pod manifest for command execution
             containers = self.pod_manifest.get("spec", {}).get("containers", [])
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self.pod_name = "sandbox-default"  # Changing the pod name to a static value, losing uniqueness

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 61 =====
```
             self._reconfigure_with_pod_manifest()
 
             # Extract container name from pod manifest for command execution
-            containers = self.pod_manifest.get("spec", {}).get("containers", [])
+            containers = None
             if containers:
                 self.container_name = containers[0]["name"]
             else:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = None
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 62 =====
```
             self._reconfigure_with_pod_manifest()
 
             # Extract container name from pod manifest for command execution
-            containers = self.pod_manifest.get("spec", {}).get("containers", [])
+            containers = self.pod_manifest.get("SPEC", {}).get("containers", [])
             if containers:
                 self.container_name = containers[0]["name"]
             else:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("SPEC", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 63 =====
```
             self._reconfigure_with_pod_manifest()
 
             # Extract container name from pod manifest for command execution
-            containers = self.pod_manifest.get("spec", {}).get("containers", [])
+            containers = self.pod_manifest.get("XXspecXX", {}).get("containers", [])
             if containers:
                 self.container_name = containers[0]["name"]
             else:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("XXspecXX", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 64 =====
```
             self._reconfigure_with_pod_manifest()
 
             # Extract container name from pod manifest for command execution
-            containers = self.pod_manifest.get("spec", {}).get("containers", [])
+            containers = self.pod_manifest.get("spec", {}).get("CONTAINERS", [])
             if containers:
                 self.container_name = containers[0]["name"]
             else:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("CONTAINERS", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 65 =====
```
             self._reconfigure_with_pod_manifest()
 
             # Extract container name from pod manifest for command execution
-            containers = self.pod_manifest.get("spec", {}).get("containers", [])
+            containers = self.pod_manifest.get("spec", {}).get("XXcontainersXX", [])
             if containers:
                 self.container_name = containers[0]["name"]
             else:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("XXcontainersXX", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 66 =====
```
             self._reconfigure_with_pod_manifest()
 
             # Extract container name from pod manifest for command execution
-            containers = self.pod_manifest.get("spec", {}).get("containers", [])
+            containers = self.pod_manifest.get("spec", {}).get(None, [])
             if containers:
                 self.container_name = containers[0]["name"]
             else:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get(None, [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 67 =====
```
             self._reconfigure_with_pod_manifest()
 
             # Extract container name from pod manifest for command execution
-            containers = self.pod_manifest.get("spec", {}).get("containers", [])
+            containers = self.pod_manifest.get(None, {}).get("containers", [])
             if containers:
                 self.container_name = containers[0]["name"]
             else:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get(None, {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 68 =====
```
 
             # Extract container name from pod manifest for command execution
             containers = self.pod_manifest.get("spec", {}).get("containers", [])
-            if containers:
+            if len(containers) > 1:  # This will only set the container name if there are multiple containers
                 self.container_name = containers[0]["name"]
             else:
                 self.container_name = "sandbox-container"  # fallback
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if len(containers) > 1:  # This will only set the container name if there are multiple containers
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False
```
===== 69 =====
```
             # Extract container name from pod manifest for command execution
             containers = self.pod_manifest.get("spec", {}).get("containers", [])
             if containers:
-                self.container_name = containers[0]["name"]
+                self.container_name = None
             else:
                 self.container_name = "sandbox-container"  # fallback
         elif container_id:
@@ -86,4 +86,4 @@             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = None
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 70 =====
```
             if containers:
                 self.container_name = containers[0]["name"]
             else:
-                self.container_name = "sandbox-container"  # fallback
+                self.container_name = "SANDBOX-CONTAINER"  # fallback
         elif container_id:
             self.pod_name = container_id
             # For existing containers, we'll need to query the pod to get container name
             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "SANDBOX-CONTAINER"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 71 =====
```
             if containers:
                 self.container_name = containers[0]["name"]
             else:
-                self.container_name = "sandbox-container"  # fallback
+                self.container_name = "XXsandbox-containerXX"  # fallback
         elif container_id:
             self.pod_name = container_id
             # For existing containers, we'll need to query the pod to get container name
             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "XXsandbox-containerXX"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 72 =====
```
             if containers:
                 self.container_name = containers[0]["name"]
             else:
-                self.container_name = "sandbox-container"  # fallback
+                self.container_name = None  # fallback
         elif container_id:
             self.pod_name = container_id
             # For existing containers, we'll need to query the pod to get container name
             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = False
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = None  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = False

```
===== 73 =====
```
             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = None
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = None

```
===== 74 =====
```
             self.container_name = None  # Will be set when connecting
 
         # For compatibility with base class
-        self.stream = False+        self.stream = True
```
```
    def __init__(
        self,  # NOSONAR (too many arguments)
        client: CoreV1Api | None = None,
        image: str | None = None,
        lang: str = SupportedLanguage.PYTHON,
        verbose: bool = False,
        kube_namespace: str = "default",
        env_vars: dict[str, str] | None = None,
        pod_manifest: dict | None = None,
        workdir: str = "/sandbox",
        security_policy: SecurityPolicy | None = None,
        default_timeout: float | None = None,
        execution_timeout: float | None = None,
        session_timeout: float | None = None,
        container_id: str | None = None,  # This will be pod_id for Kubernetes
        skip_environment_setup: bool = False,
        **kwargs: Any,
    ) -> None:
        r"""Initialize Kubernetes session.

        Args:
            client (CoreV1Api | None): The Kubernetes client to use.
            image (str | None): The image to use.
            lang (str): The language to use.
            verbose (bool): Whether to enable verbose output.
            kube_namespace (str): The Kubernetes namespace to use.
            env_vars (dict[str, str] | None): The environment variables to use.
            pod_manifest (dict | None): The Kubernetes pod manifest to use.
            workdir (str): The working directory to use.
            security_policy (SecurityPolicy | None): The security policy to use.
            default_timeout (float | None): The default timeout to use.
            execution_timeout (float | None): The execution timeout to use.
            session_timeout (float | None): The session timeout to use.
            container_id (str | None): ID of existing pod to connect to.
            skip_environment_setup (bool): Skip language-specific environment setup.
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        config = SessionConfig(
            image=image,
            lang=SupportedLanguage(lang.upper()),
            verbose=verbose,
            workdir=workdir,
            security_policy=security_policy,
            default_timeout=default_timeout,
            execution_timeout=execution_timeout,
            session_timeout=session_timeout,
            container_id=container_id,
            skip_environment_setup=skip_environment_setup,
        )

        super().__init__(config=config, **kwargs)

        if not client:
            self._log("Using local Kubernetes context since client is not provided.")
            from kubernetes import config as k8s_config

            k8s_config.load_kube_config()
            self.client = CoreV1Api()
        else:
            self.client = client

        self.kube_namespace = kube_namespace
        self.container_api = KubernetesContainerAPI(self.client, kube_namespace)

        # Generate unique pod name (only if not using existing pod)
        if not self.using_existing_container:
            short_uuid = uuid.uuid4().hex[:8]
            self.pod_name = f"sandbox-{lang.lower()}-{short_uuid}"
            self.env_vars = env_vars
            self.pod_manifest = pod_manifest or self._default_pod_manifest()
            self._reconfigure_with_pod_manifest()

            # Extract container name from pod manifest for command execution
            containers = self.pod_manifest.get("spec", {}).get("containers", [])
            if containers:
                self.container_name = containers[0]["name"]
            else:
                self.container_name = "sandbox-container"  # fallback
        elif container_id:
            self.pod_name = container_id
            # For existing containers, we'll need to query the pod to get container name
            self.container_name = None  # Will be set when connecting

        # For compatibility with base class
        self.stream = True

```
