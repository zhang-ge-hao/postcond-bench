https://github.com/vndee/llm-sandbox/blob/218b9d3d8523bac44e60e241ab72f7e160f8ad30/./llm_sandbox/mcp_server/server.py#L57-L114
```
🈚️

run subprocess
```
```
@icontract.snapshot(lambda code: code, name="input_code")
@icontract.snapshot(lambda language: language, name="input_language")
@icontract.snapshot(lambda libraries: libraries, name="input_libraries")
@icontract.snapshot(lambda timeout: timeout, name="input_timeout")
@icontract.ensure(lambda result: isinstance(result, list) and len(result) >= 1)
@icontract.ensure(lambda result: isinstance(result[-1], TextContent) and result[-1].type == "text")
@icontract.ensure(lambda result: (lambda j: isinstance(j, dict) and all(k in j for k in ("exit_code", "stdout", "stderr")))(__import__("json").loads(result[-1].text)))
@icontract.ensure(lambda result: isinstance(__import__("json").loads(result[-1].text)["exit_code"], int))
@icontract.ensure(lambda result: "plots" not in __import__("json").loads(result[-1].text))
@icontract.ensure(lambda result, language: (not _supports_visualization(language)) or (isinstance(result[0], ImageContent) or ("Plot" not in __import__("json").loads(result[-1].text)["stdout"])))
@icontract.ensure(lambda result: (not isinstance(result[0], ImageContent)) or (result[0].type == "image" and isinstance(result[0].data, str) and bool(result[0].data) and isinstance(result[0].mimeType, str) and result[0].mimeType.startswith("image/")))
@icontract.ensure(lambda result: (not isinstance(result[0], ImageContent)) or isinstance(result[-1], TextContent))
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 80, 81, 82, 83, 84, 85, 86, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 109, 110, 111, 112, 113, 114, 115, 118, 119, 120, 121, 122, 123, 124, 125, 127]
===== 0 =====
```
         List of content items including execution results and any generated visualizations
 
     """
-    results: list[ImageContent | TextContent] = []
+    results: list[ImageContent | TextContent] = None
 
     try:
         use_artifact_session = _supports_visualization(language)
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = None

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 1 =====
```
     results: list[ImageContent | TextContent] = []
 
     try:
-        use_artifact_session = _supports_visualization(language)
+        use_artifact_session = False  # Always use the standard session
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = False  # Always use the standard session
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 2 =====
```
     results: list[ImageContent | TextContent] = []
 
     try:
-        use_artifact_session = _supports_visualization(language)
+        use_artifact_session = None
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = None
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 3 =====
```
     results: list[ImageContent | TextContent] = []
 
     try:
-        use_artifact_session = _supports_visualization(language)
+        use_artifact_session = _supports_visualization("python")
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization("python")
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 4 =====
```
     results: list[ImageContent | TextContent] = []
 
     try:
-        use_artifact_session = _supports_visualization(language)
+        use_artifact_session = _supports_visualization(None)
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(None)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 5 =====
```
     results: list[ImageContent | TextContent] = []
 
     try:
-        use_artifact_session = _supports_visualization(language)
+        use_artifact_session = _supports_visualization(language) or language == "javascript"
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language) or language == "javascript"
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 6 =====
```
     results: list[ImageContent | TextContent] = []
 
     try:
-        use_artifact_session = _supports_visualization(language)
+        use_artifact_session = not _supports_visualization(language)
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = not _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 7 =====
```
 
     try:
         use_artifact_session = _supports_visualization(language)
-        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
+        session_cls = None
 
         with session_cls(
             lang=language,
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = None

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 8 =====
```
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
-            lang=language,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 9 =====
```
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
-            lang=language,
+            lang="python",  # Hardcoding the language to Python, ignoring the provided language parameter
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang="python",  # Hardcoding the language to Python, ignoring the provided language parameter
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 10 =====
```
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
-            lang=language,
+            lang=None,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=None,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 11 =====
```
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
-            lang=language,
+            lang=None,  # Setting the language to None, which may cause issues during execution
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=None,  # Setting the language to None, which may cause issues during execution
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 12 =====
```
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
-            lang=language,
+            lang=language + "extra",  # Appending extra text to the language, leading to invalid language identifiers
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language + "extra",  # Appending extra text to the language, leading to invalid language identifiers
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 13 =====
```
         session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession
 
         with session_cls(
-            lang=language,
+            lang=language.upper(),  # Converting the language to uppercase, which may not match expected values
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language.upper(),  # Converting the language to uppercase, which may not match expected values
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 14 =====
```
 
         with session_cls(
             lang=language,
-            keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 15 =====
```
 
         with session_cls(
             lang=language,
-            keep_template=_get_keep_template(),
+            keep_template="true",
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template="true",
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 16 =====
```
 
         with session_cls(
             lang=language,
-            keep_template=_get_keep_template(),
+            keep_template=False,
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=False,
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 17 =====
```
 
         with session_cls(
             lang=language,
-            keep_template=_get_keep_template(),
+            keep_template=None,
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=None,
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 18 =====
```
 
         with session_cls(
             lang=language,
-            keep_template=_get_keep_template(),
+            keep_template=None,
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=None,
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 19 =====
```
         with session_cls(
             lang=language,
             keep_template=_get_keep_template(),
-            commit_container=_get_commit_container(),
+            commit_container="true",
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container="true",
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 20 =====
```
         with session_cls(
             lang=language,
             keep_template=_get_keep_template(),
-            commit_container=_get_commit_container(),
+            commit_container=False,
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=False,
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 21 =====
```
         with session_cls(
             lang=language,
             keep_template=_get_keep_template(),
-            commit_container=_get_commit_container(),
+            commit_container=None,
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=None,
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 22 =====
```
         with session_cls(
             lang=language,
             keep_template=_get_keep_template(),
-            commit_container=_get_commit_container(),
+            commit_container=None,
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=None,
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 23 =====
```
         with session_cls(
             lang=language,
             keep_template=_get_keep_template(),
-            commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 24 =====
```
             lang=language,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
-            verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 25 =====
```
             lang=language,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
-            verbose=False,
+            verbose="false",
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose="false",
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 26 =====
```
             lang=language,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
-            verbose=False,
+            verbose="yes",
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose="yes",
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 27 =====
```
             lang=language,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
-            verbose=False,
+            verbose=1,
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=1,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 28 =====
```
             lang=language,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
-            verbose=False,
+            verbose=None,
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=None,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 29 =====
```
             lang=language,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
-            verbose=False,
+            verbose=None,
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=None,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 30 =====
```
             lang=language,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
-            verbose=False,
+            verbose=True,
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=True,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 31 =====
```
             lang=language,
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
-            verbose=False,
+            verbose=True,
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=True,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 32 =====
```
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
-            backend=_get_backend(),
+            backend="invalid_backend",
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
         ) as session:
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend="invalid_backend",
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 33 =====
```
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
-            backend=_get_backend(),
+            backend=None,
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
         ) as session:
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=None,
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 34 =====
```
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
-            backend=_get_backend(),
+            backend=None,
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
         ) as session:
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=None,
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 35 =====
```
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
-            backend=_get_backend(),
+            backend=os.environ.get("BACKEND", "invalid"),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
         ) as session:
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=os.environ.get("BACKEND", "invalid"),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 36 =====
```
             keep_template=_get_keep_template(),
             commit_container=_get_commit_container(),
             verbose=False,
-            backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
         ) as session:
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 37 =====
```
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
-            session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 38 =====
```
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
-            session_timeout=timeout,
+            session_timeout="30",
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout="30",
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 39 =====
```
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
-            session_timeout=timeout,
+            session_timeout=0,
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=0,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 40 =====
```
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
-            session_timeout=timeout,
+            session_timeout=None,
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=None,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 41 =====
```
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
-            session_timeout=timeout,
+            session_timeout=None,
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=None,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 42 =====
```
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
-            session_timeout=timeout,
+            session_timeout=timeout + 10,
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout + 10,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 43 =====
```
             commit_container=_get_commit_container(),
             verbose=False,
             backend=_get_backend(),
-            session_timeout=timeout,
+            session_timeout=timeout - 5,
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout - 5,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 44 =====
```
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
-            kube_namespace=_get_kube_namespace(),
-        ) as session:
+            ) as session:
             result = session.run(
                 code=code,
                 libraries=libraries or [],
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 45 =====
```
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
-            kube_namespace=_get_kube_namespace(),
+            kube_namespace=None,
         ) as session:
             result = session.run(
                 code=code,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=None,
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 46 =====
```
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
-            kube_namespace=_get_kube_namespace(),
+            kube_namespace=None,
         ) as session:
             result = session.run(
                 code=code,
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=None,
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 47 =====
```
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
-            kube_namespace=_get_kube_namespace(),
+            kube_namespace=_get_kube_namespace() if os.environ.get("USE_KUBE", "false") == "true" else None,
         ) as session:
             result = session.run(
                 code=code,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace() if os.environ.get("USE_KUBE", "false") == "true" else None,
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 48 =====
```
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
-            kube_namespace=_get_kube_namespace(),
+            kube_namespace=_get_kube_namespace().upper(),
         ) as session:
             result = session.run(
                 code=code,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace().upper(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 49 =====
```
             verbose=False,
             backend=_get_backend(),
             session_timeout=timeout,
-            kube_namespace=_get_kube_namespace(),
+            kube_namespace=os.environ.get("NAMESPACE", "production"),
         ) as session:
             result = session.run(
                 code=code,
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=os.environ.get("NAMESPACE", "production"),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 50 =====
```
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
-        ) as session:
+        ) as sandbox_session:
             result = session.run(
                 code=code,
                 libraries=libraries or [],
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as sandbox_session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 51 =====
```
             backend=_get_backend(),
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
-        ) as session:
+        ) as session_cls:
             result = session.run(
                 code=code,
                 libraries=libraries or [],
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session_cls:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 52 =====
```
             session_timeout=timeout,
             kube_namespace=_get_kube_namespace(),
         ) as session:
-            result = session.run(
-                code=code,
-                libraries=libraries or [],
-                timeout=timeout,
-            )
+            result = None
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
                 plot = result.plots[0]
@@ -55,4 +51,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = None

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 53 =====
```
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
-                code=code,
+                code="",  # This will execute an empty code string, leading to no meaningful output.
                 libraries=libraries or [],
                 timeout=timeout,
             )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code="",  # This will execute an empty code string, leading to no meaningful output.
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 54 =====
```
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
-                code=code,
+                code="print('Hello World')",  # This hardcodes a print statement, ignoring the provided code.
                 libraries=libraries or [],
                 timeout=timeout,
             )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code="print('Hello World')",  # This hardcodes a print statement, ignoring the provided code.
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 55 =====
```
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
-                code=code,
+                code=None,
                 libraries=libraries or [],
                 timeout=timeout,
             )
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=None,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 56 =====
```
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
-                code=code,
+                code=None,  # Passing None will likely cause the execution to fail silently or produce unexpected results.
                 libraries=libraries or [],
                 timeout=timeout,
             )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=None,  # Passing None will likely cause the execution to fail silently or produce unexpected results.
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 57 =====
```
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
-                code=code,
+                code=code + " ",  # This adds a space to the code, which may alter its intended functionality.
                 libraries=libraries or [],
                 timeout=timeout,
             )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code + " ",  # This adds a space to the code, which may alter its intended functionality.
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 58 =====
```
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
-                code=code,
+                code=code[::-1],  # This reverses the code string, which will likely lead to incorrect execution.
                 libraries=libraries or [],
                 timeout=timeout,
             )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code[::-1],  # This reverses the code string, which will likely lead to incorrect execution.
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 59 =====
```
             kube_namespace=_get_kube_namespace(),
         ) as session:
             result = session.run(
-                code=code,
                 libraries=libraries or [],
                 timeout=timeout,
             )
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 60 =====
```
         ) as session:
             result = session.run(
                 code=code,
-                libraries=libraries or [],
+                libraries=None,
                 timeout=timeout,
             )
 
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=None,
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 61 =====
```
         ) as session:
             result = session.run(
                 code=code,
-                libraries=libraries or [],
+                libraries=libraries and [],
                 timeout=timeout,
             )
 
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries and [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 62 =====
```
         ) as session:
             result = session.run(
                 code=code,
-                libraries=libraries or [],
+                libraries=libraries if len(libraries) > 0 else [],
                 timeout=timeout,
             )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries if len(libraries) > 0 else [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 63 =====
```
         ) as session:
             result = session.run(
                 code=code,
-                libraries=libraries or [],
+                libraries=libraries if libraries else None,
                 timeout=timeout,
             )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries if libraries else None,
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 64 =====
```
         ) as session:
             result = session.run(
                 code=code,
-                libraries=libraries or [],
+                libraries=libraries or ["default_library"],
                 timeout=timeout,
             )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or ["default_library"],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 65 =====
```
         ) as session:
             result = session.run(
                 code=code,
-                libraries=libraries or [],
+                libraries=libraries or ["numpy"],
                 timeout=timeout,
             )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or ["numpy"],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 66 =====
```
         ) as session:
             result = session.run(
                 code=code,
-                libraries=libraries or [],
                 timeout=timeout,
             )
 
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 67 =====
```
             result = session.run(
                 code=code,
                 libraries=libraries or [],
-                timeout=timeout,
-            )
+                )
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
                 plot = result.plots[0]
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 68 =====
```
             result = session.run(
                 code=code,
                 libraries=libraries or [],
-                timeout=timeout,
+                timeout="thirty",  # Incorrect type for timeout
             )
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout="thirty",  # Incorrect type for timeout
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 69 =====
```
             result = session.run(
                 code=code,
                 libraries=libraries or [],
-                timeout=timeout,
+                timeout=-10,  # Negative timeout value
             )
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=-10,  # Negative timeout value
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 70 =====
```
             result = session.run(
                 code=code,
                 libraries=libraries or [],
-                timeout=timeout,
+                timeout=0,
             )
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=0,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 71 =====
```
             result = session.run(
                 code=code,
                 libraries=libraries or [],
-                timeout=timeout,
+                timeout=60,  # Exceeds the intended timeout limit
             )
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=60,  # Exceeds the intended timeout limit
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 72 =====
```
             result = session.run(
                 code=code,
                 libraries=libraries or [],
-                timeout=timeout,
+                timeout=None,
             )
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=None,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 73 =====
```
             result = session.run(
                 code=code,
                 libraries=libraries or [],
-                timeout=timeout,
+                timeout=None,  # Passes a None value instead of an integer
             )
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=None,  # Passes a None value instead of an integer
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 74 =====
```
                 timeout=timeout,
             )
 
-            if use_artifact_session and hasattr(result, "plots") and result.plots:
+            if use_artifact_session and hasattr("plots") and result.plots:
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr("plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 80 =====
```
                 timeout=timeout,
             )
 
-            if use_artifact_session and hasattr(result, "plots") and result.plots:
+            if use_artifact_session and hasattr(result, "plots") or result.plots:
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") or result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 81 =====
```
                 timeout=timeout,
             )
 
-            if use_artifact_session and hasattr(result, "plots") and result.plots:
+            if use_artifact_session and hasattr(result, "plots"):
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots"):
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 82 =====
```
                 timeout=timeout,
             )
 
-            if use_artifact_session and hasattr(result, "plots") and result.plots:
+            if use_artifact_session and hasattr(result, ) and result.plots:
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, ) and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 83 =====
```
                 timeout=timeout,
             )
 
-            if use_artifact_session and hasattr(result, "plots") and result.plots:
+            if use_artifact_session and hasattr(result, None) and result.plots:
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, None) and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 84 =====
```
                 timeout=timeout,
             )
 
-            if use_artifact_session and hasattr(result, "plots") and result.plots:
+            if use_artifact_session or hasattr(result, "plots") and result.plots:
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session or hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 85 =====
```
             )
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
-                plot = result.plots[0]
+                plot = None
                 results.append(
                     ImageContent(
                         data=plot.content_base64,
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = None
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 86 =====
```
             )
 
             if use_artifact_session and hasattr(result, "plots") and result.plots:
-                plot = result.plots[0]
+                plot = result.plots[1]
                 results.append(
                     ImageContent(
                         data=plot.content_base64,
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[1]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 88 =====
```
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
-                        data=plot.content_base64,
+                        data=None,
                         mimeType=f"image/{plot.format.value}",
                         type="image",
                     )
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=None,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 89 =====
```
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
-                        data=plot.content_base64,
+                        data=None,  # Sets the data to None, which will not provide any valid content
                         mimeType=f"image/{plot.format.value}",
                         type="image",
                     )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=None,  # Sets the data to None, which will not provide any valid content
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 90 =====
```
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
-                        data=plot.content_base64,
+                        data=plot.content_base64 + "extra_data",  # Appends extra data to the content, which may not be valid
                         mimeType=f"image/{plot.format.value}",
                         type="image",
                     )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64 + "extra_data",  # Appends extra data to the content, which may not be valid
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 91 =====
```
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
-                        data=plot.content_base64,
+                        data=plot.content_base64.upper(),  # Converts the content to uppercase, altering the original data
                         mimeType=f"image/{plot.format.value}",
                         type="image",
                     )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64.upper(),  # Converts the content to uppercase, altering the original data
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 92 =====
```
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
-                        data=plot.content_base64,
+                        data=plot.content_base64[:10],  # Only takes the first 10 characters of the content
                         mimeType=f"image/{plot.format.value}",
                         type="image",
                     )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64[:10],  # Only takes the first 10 characters of the content
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 93 =====
```
                 plot = result.plots[0]
                 results.append(
                     ImageContent(
-                        data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
                         type="image",
                     )
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 94 =====
```
                 results.append(
                     ImageContent(
                         data=plot.content_base64,
-                        mimeType=f"image/{plot.format.value}",
+                        mimeType="image/jpeg",  # Hardcoded MIME type that may not match the actual format
                         type="image",
                     )
                 )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType="image/jpeg",  # Hardcoded MIME type that may not match the actual format
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 95 =====
```
                 results.append(
                     ImageContent(
                         data=plot.content_base64,
-                        mimeType=f"image/{plot.format.value}",
+                        mimeType=None,
                         type="image",
                     )
                 )
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=None,
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 96 =====
```
                 results.append(
                     ImageContent(
                         data=plot.content_base64,
-                        mimeType=f"image/{plot.format.value}",
+                        mimeType=f"image/{plot.format.value}; charset=utf-8",  # Adding an invalid charset parameter to the MIME type
                         type="image",
                     )
                 )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}; charset=utf-8",  # Adding an invalid charset parameter to the MIME type
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 97 =====
```
                 results.append(
                     ImageContent(
                         data=plot.content_base64,
-                        mimeType=f"image/{plot.format.value}",
+                        mimeType=f"image/{plot.format}",  # Missing .value, which may lead to incorrect MIME type
                         type="image",
                     )
                 )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format}",  # Missing .value, which may lead to incorrect MIME type
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 98 =====
```
                 results.append(
                     ImageContent(
                         data=plot.content_base64,
-                        mimeType=f"image/{plot.format.value}",
                         type="image",
                     )
                 )
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 99 =====
```
                     ImageContent(
                         data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
-                        type="image",
-                    )
+                        )
                 )
 
             results.append(TextContent(text=result.to_json(include_plots=False), type="text"))
@@ -55,4 +54,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 100 =====
```
                     ImageContent(
                         data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
-                        type="image",
+                        type="IMAGE",
                     )
                 )
 
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="IMAGE",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 101 =====
```
                     ImageContent(
                         data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
-                        type="image",
+                        type="XXimageXX",
                     )
                 )
 
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="XXimageXX",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 102 =====
```
                     ImageContent(
                         data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
-                        type="image",
+                        type="application/json",
                     )
                 )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="application/json",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 103 =====
```
                     ImageContent(
                         data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
-                        type="image",
+                        type="image/jpeg",
                     )
                 )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image/jpeg",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 104 =====
```
                     ImageContent(
                         data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
-                        type="image",
+                        type="image/png",
                     )
                 )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image/png",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 105 =====
```
                     ImageContent(
                         data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
-                        type="image",
+                        type="text/html",
                     )
                 )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="text/html",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 106 =====
```
                     ImageContent(
                         data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
-                        type="image",
+                        type="text/plain",
                     )
                 )
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="text/plain",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 107 =====
```
                     ImageContent(
                         data=plot.content_base64,
                         mimeType=f"image/{plot.format.value}",
-                        type="image",
+                        type=None,
                     )
                 )
 
@@ -55,4 +55,4 @@         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type=None,
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 109 =====
```
                     )
                 )
 
-            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))
+            results.append(TextContent(text="Execution completed successfully", type="text"))
 
     except Exception as e:
         logger.exception("Error executing code")
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text="Execution completed successfully", type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 110 =====
```
                     )
                 )
 
-            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))
+            results.append(TextContent(text=None, type="text"))
 
     except Exception as e:
         logger.exception("Error executing code")
         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=None, type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 111 =====
```
                     )
                 )
 
-            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))
+            results.append(TextContent(text=result.to_json(include_plots=False), ))
 
     except Exception as e:
         logger.exception("Error executing code")
         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), ))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 112 =====
```
                     )
                 )
 
-            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))
+            results.append(TextContent(text=result.to_json(include_plots=False), type="TEXT"))
 
     except Exception as e:
         logger.exception("Error executing code")
         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="TEXT"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 113 =====
```
                     )
                 )
 
-            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))
+            results.append(TextContent(text=result.to_json(include_plots=False), type="XXtextXX"))
 
     except Exception as e:
         logger.exception("Error executing code")
         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="XXtextXX"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 114 =====
```
                     )
                 )
 
-            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))
+            results.append(TextContent(text=result.to_json(include_plots=False), type="image"))
 
     except Exception as e:
         logger.exception("Error executing code")
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="image"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 115 =====
```
                     )
                 )
 
-            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))
+            results.append(TextContent(text=result.to_json(include_plots=False), type=None))
 
     except Exception as e:
         logger.exception("Error executing code")
         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type=None))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 118 =====
```
                     )
                 )
 
-            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))
+            results.append(TextContent(type="text"))
 
     except Exception as e:
         logger.exception("Error executing code")
         return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 119 =====
```
 
     except Exception as e:
         logger.exception("Error executing code")
-        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
+        return [TextContent(text="An error occurred during execution.", type="text")]
 
     else:
         return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text="An error occurred during execution.", type="text")]

    else:
        return results
```
===== 120 =====
```
 
     except Exception as e:
         logger.exception("Error executing code")
-        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
+        return [TextContent(text=ExecutionResult(exit_code=0, stderr=str(e)).to_json(), type="text")]
 
     else:
         return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=0, stderr=str(e)).to_json(), type="text")]

    else:
        return results
```
===== 121 =====
```
 
     except Exception as e:
         logger.exception("Error executing code")
-        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
+        return [TextContent(text=ExecutionResult(exit_code=1, ).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, ).to_json(), type="text")]

    else:
        return results

```
===== 122 =====
```
 
     except Exception as e:
         logger.exception("Error executing code")
-        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
+        return [TextContent(text=ExecutionResult(exit_code=1, stderr="Execution failed").to_json(), type="text")]
 
     else:
         return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr="Execution failed").to_json(), type="text")]

    else:
        return results
```
===== 123 =====
```
 
     except Exception as e:
         logger.exception("Error executing code")
-        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
+        return [TextContent(text=ExecutionResult(exit_code=1, stderr=None).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=None).to_json(), type="text")]

    else:
        return results

```
===== 124 =====
```
 
     except Exception as e:
         logger.exception("Error executing code")
-        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
+        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(None)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(None)).to_json(), type="text")]

    else:
        return results

```
===== 125 =====
```
 
     except Exception as e:
         logger.exception("Error executing code")
-        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
+        return [TextContent(text=ExecutionResult(exit_code=2, stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(exit_code=2, stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
===== 127 =====
```
 
     except Exception as e:
         logger.exception("Error executing code")
-        return [TextContent(text=ExecutionResult(exit_code=1, stderr=str(e)).to_json(), type="text")]
+        return [TextContent(text=ExecutionResult(stderr=str(e)).to_json(), type="text")]
 
     else:
-        return results+        return results
```
```
@mcp.tool()
def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    """Execute code in a secure sandbox environment and automatic visualization capture.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, java, cpp, go, r, ruby)
        libraries: List of libraries/packages to install
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        List of content items including execution results and any generated visualizations

    """
    results: list[ImageContent | TextContent] = []

    try:
        use_artifact_session = _supports_visualization(language)
        session_cls = ArtifactSandboxSession if use_artifact_session else SandboxSession

        with session_cls(
            lang=language,
            keep_template=_get_keep_template(),
            commit_container=_get_commit_container(),
            verbose=False,
            backend=_get_backend(),
            session_timeout=timeout,
            kube_namespace=_get_kube_namespace(),
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )

            if use_artifact_session and hasattr(result, "plots") and result.plots:
                plot = result.plots[0]
                results.append(
                    ImageContent(
                        data=plot.content_base64,
                        mimeType=f"image/{plot.format.value}",
                        type="image",
                    )
                )

            results.append(TextContent(text=result.to_json(include_plots=False), type="text"))

    except Exception as e:
        logger.exception("Error executing code")
        return [TextContent(text=ExecutionResult(stderr=str(e)).to_json(), type="text")]

    else:
        return results

```
