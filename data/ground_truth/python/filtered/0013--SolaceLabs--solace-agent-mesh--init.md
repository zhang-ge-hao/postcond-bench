https://github.com/SolaceLabs/solace-agent-mesh/blob/6564748e81c0625394b55124c4d80e4af2f6042b/./cli/commands/init_cmd/__init__.py#L204-L439
```
🈚️
No icontract
```
```
None
```
[0, 1, 2, 3, 4, 5]
===== 0 =====
```
             )
             kwargs["broker_type"] = "dev"
 
-    skip_interactive_val = kwargs.pop("skip", False)
+    skip_interactive_val = kwargs.pop(False)
     use_web_based_init_val = kwargs.pop("gui", False)
 
     run_init_flow(
         skip_interactive=skip_interactive_val,
         use_web_based_init_flag=use_web_based_init_val,
         **kwargs,
-    )+    )
```
```
@click.command(name="init")
@click.option(
    "--skip",
    is_flag=True,
    default=False,
    help="Non-interactive mode. Skip all prompts and use default values where applicable.",
)
@click.option(
    "--gui",
    is_flag=True,
    default=False,
    help="Launch the browser-based initialization interface.",
)
@click.option("--llm-service-endpoint", type=str, help="LLM Service Endpoint URL.")
@click.option("--llm-service-api-key", type=str, help="LLM Service API Key.")
@click.option(
    "--llm-service-planning-model-name", type=str, help="LLM Planning Model Name."
)
@click.option(
    "--llm-service-general-model-name", type=str, help="LLM General Model Name."
)
@click.option("--namespace", type=str, help="Namespace for the project.")
@click.option(
    "--broker-type",
    type=click.Choice(
        ["1", "2", "3", "solace", "container", "dev_mode", "dev_broker", "dev"],
        case_sensitive=False,
    ),
    help="Broker type: 1/solace (existing), 2/container (new local), 3/dev (dev mode).",
)
@click.option("--broker-url", type=str, help="Solace broker URL endpoint.")
@click.option("--broker-vpn", type=str, help="Solace broker VPN name.")
@click.option("--broker-username", type=str, help="Solace broker username.")
@click.option("--broker-password", type=str, help="Solace broker password.")
@click.option(
    "--container-engine",
    type=click.Choice(["podman", "docker"], case_sensitive=False),
    help="Container engine for local broker.",
)
@click.option(
    "--dev-mode",
    "dev_mode_flag",
    is_flag=True,
    help="Shortcut to select dev mode for broker (equivalent to --broker-type 3/dev).",
)
@click.option("--agent-name", type=str, help="Agent name for the main orchestrator.")
@click.option(
    "--supports-streaming",
    is_flag=True,
    help="Enable streaming support for the agent.",
    default=None,
)
@click.option(
    "--session-service-type",
    type=click.Choice(["memory", "vertex_rag", "sql"]),
    help="Session service type.",
)
@click.option(
    "--session-service-behavior",
    type=click.Choice(["PERSISTENT", "RUN_BASED"]),
    help="Session service behavior.",
)
@click.option(
    "--artifact-service-type",
    type=click.Choice(["memory", "filesystem", "gcs", "s3"]),
    help="Artifact service type.",
)
@click.option(
    "--artifact-service-base-path",
    type=str,
    help="Artifact service base path (for filesystem type).",
)
@click.option(
    "--artifact-service-bucket-name",
    type=str,
    help="S3 bucket name (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-endpoint-url",
    type=str,
    help="S3 endpoint URL (for s3 artifact service type, optional for AWS S3).",
)
@click.option(
    "--artifact-service-region",
    type=str,
    help="S3 region (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-scope",
    type=click.Choice(["namespace", "app", "custom"]),
    help="Artifact service scope.",
)
@click.option(
    "--artifact-handling-mode",
    type=click.Choice(["ignore", "embed", "reference"]),
    help="Artifact handling mode.",
)
@click.option(
    "--enable-embed-resolution",
    is_flag=True,
    help="Enable embed resolution.",
    default=None,
)
@click.option(
    "--enable-artifact-content-instruction",
    is_flag=True,
    help="Enable artifact content instruction.",
    default=None,
)
@click.option(
    "--enable-builtin-artifact-tools",
    is_flag=True,
    help="Enable built-in artifact tools.",
    default=None,
)
@click.option(
    "--enable-builtin-data-tools",
    is_flag=True,
    help="Enable built-in data tools.",
    default=None,
)
@click.option("--agent-card-description", type=str, help="Agent card description.")
@click.option(
    "--agent-card-default-input-modes",
    type=str,
    help="Agent card default input modes (comma-separated).",
)
@click.option(
    "--agent-card-default-output-modes",
    type=str,
    help="Agent card default output modes (comma-separated).",
)
@click.option(
    "--agent-discovery-enabled",
    is_flag=True,
    help="Enable agent discovery.",
    default=None,
)
@click.option(
    "--agent-card-publishing-interval",
    type=int,
    help="Agent card publishing interval (seconds).",
)
@click.option(
    "--inter-agent-communication-allow-list",
    type=str,
    help="Inter-agent communication allow list (comma-separated, use * for all).",
)
@click.option(
    "--inter-agent-communication-deny-list",
    type=str,
    help="Inter-agent communication deny list (comma-separated).",
)
@click.option(
    "--inter-agent-communication-timeout",
    type=int,
    help="Inter-agent communication timeout (seconds).",
)
@click.option(
    "--add-webui-gateway",
    is_flag=True,
    default=None,
    help="Add a default Web UI gateway configuration.",
)
@click.option(
    "--webui-session-secret-key", type=str, help="Session secret key for Web UI."
)
@click.option("--webui-fastapi-host", type=str, help="Host for Web UI FastAPI server.")
@click.option("--webui-fastapi-port", type=int, help="Port for Web UI FastAPI server.")
@click.option(
    "--webui-fastapi-https-port", type=int, help="HTTPS port for Web UI FastAPI server."
)
@click.option("--webui-ssl-keyfile", type=str, help="SSL key file path for Web UI.")
@click.option(
    "--webui-ssl-certfile", type=str, help="SSL certificate file path for Web UI."
)
@click.option(
    "--webui-ssl-keyfile-password", type=str, help="SSL key file passphrase for Web UI."
)
@click.option(
    "--webui-enable-embed-resolution",
    is_flag=True,
    default=None,
    help="Enable embed resolution for Web UI.",
)
@click.option(
    "--webui-frontend-welcome-message",
    type=str,
    help="Frontend welcome message for Web UI.",
)
@click.option(
    "--webui-frontend-bot-name", type=str, help="Frontend bot name for Web UI."
)
@click.option(
    "--webui-frontend-collect-feedback",
    is_flag=True,
    default=None,
    help="Enable feedback collection in Web UI.",
)
@click.option(
    "--web-ui-gateway-database-url",
    type=str,
    help="Database URL for the WebUI Gateway.",
)
@click.option(
    "--orchestrator-database-url",
    type=str,
    help="Database URL for the Orchestrator.",
)
def init(**kwargs):
    """
    Initialize a new Solace application project.
    Creates a directory structure, default configuration files, and a .env file.
    """
    use_web_based_init_val = kwargs.get("gui", False)

    if kwargs.get("dev_mode_flag"):
        if kwargs.get("broker_type") is None:
            kwargs["broker_type"] = "dev"
        elif kwargs.get("broker_type") not in ["3", "dev", "dev_mode", "dev_broker"]:
            click.echo(
                click.style(
                    f"Warning: --dev-mode flag is set, but --broker-type is also set to '{kwargs.get('broker_type')}'. Dev mode will be used for broker configuration.",
                    fg="yellow",
                )
            )
            kwargs["broker_type"] = "dev"

    skip_interactive_val = kwargs.pop(False)
    use_web_based_init_val = kwargs.pop("gui", False)

    run_init_flow(
        skip_interactive=skip_interactive_val,
        use_web_based_init_flag=use_web_based_init_val,
        **kwargs,
    )

```
===== 1 =====
```
             kwargs["broker_type"] = "dev"
 
     skip_interactive_val = kwargs.pop("skip", False)
-    use_web_based_init_val = kwargs.pop("gui", False)
+    use_web_based_init_val = kwargs.pop(False)
 
     run_init_flow(
         skip_interactive=skip_interactive_val,
         use_web_based_init_flag=use_web_based_init_val,
         **kwargs,
-    )+    )
```
```
@click.command(name="init")
@click.option(
    "--skip",
    is_flag=True,
    default=False,
    help="Non-interactive mode. Skip all prompts and use default values where applicable.",
)
@click.option(
    "--gui",
    is_flag=True,
    default=False,
    help="Launch the browser-based initialization interface.",
)
@click.option("--llm-service-endpoint", type=str, help="LLM Service Endpoint URL.")
@click.option("--llm-service-api-key", type=str, help="LLM Service API Key.")
@click.option(
    "--llm-service-planning-model-name", type=str, help="LLM Planning Model Name."
)
@click.option(
    "--llm-service-general-model-name", type=str, help="LLM General Model Name."
)
@click.option("--namespace", type=str, help="Namespace for the project.")
@click.option(
    "--broker-type",
    type=click.Choice(
        ["1", "2", "3", "solace", "container", "dev_mode", "dev_broker", "dev"],
        case_sensitive=False,
    ),
    help="Broker type: 1/solace (existing), 2/container (new local), 3/dev (dev mode).",
)
@click.option("--broker-url", type=str, help="Solace broker URL endpoint.")
@click.option("--broker-vpn", type=str, help="Solace broker VPN name.")
@click.option("--broker-username", type=str, help="Solace broker username.")
@click.option("--broker-password", type=str, help="Solace broker password.")
@click.option(
    "--container-engine",
    type=click.Choice(["podman", "docker"], case_sensitive=False),
    help="Container engine for local broker.",
)
@click.option(
    "--dev-mode",
    "dev_mode_flag",
    is_flag=True,
    help="Shortcut to select dev mode for broker (equivalent to --broker-type 3/dev).",
)
@click.option("--agent-name", type=str, help="Agent name for the main orchestrator.")
@click.option(
    "--supports-streaming",
    is_flag=True,
    help="Enable streaming support for the agent.",
    default=None,
)
@click.option(
    "--session-service-type",
    type=click.Choice(["memory", "vertex_rag", "sql"]),
    help="Session service type.",
)
@click.option(
    "--session-service-behavior",
    type=click.Choice(["PERSISTENT", "RUN_BASED"]),
    help="Session service behavior.",
)
@click.option(
    "--artifact-service-type",
    type=click.Choice(["memory", "filesystem", "gcs", "s3"]),
    help="Artifact service type.",
)
@click.option(
    "--artifact-service-base-path",
    type=str,
    help="Artifact service base path (for filesystem type).",
)
@click.option(
    "--artifact-service-bucket-name",
    type=str,
    help="S3 bucket name (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-endpoint-url",
    type=str,
    help="S3 endpoint URL (for s3 artifact service type, optional for AWS S3).",
)
@click.option(
    "--artifact-service-region",
    type=str,
    help="S3 region (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-scope",
    type=click.Choice(["namespace", "app", "custom"]),
    help="Artifact service scope.",
)
@click.option(
    "--artifact-handling-mode",
    type=click.Choice(["ignore", "embed", "reference"]),
    help="Artifact handling mode.",
)
@click.option(
    "--enable-embed-resolution",
    is_flag=True,
    help="Enable embed resolution.",
    default=None,
)
@click.option(
    "--enable-artifact-content-instruction",
    is_flag=True,
    help="Enable artifact content instruction.",
    default=None,
)
@click.option(
    "--enable-builtin-artifact-tools",
    is_flag=True,
    help="Enable built-in artifact tools.",
    default=None,
)
@click.option(
    "--enable-builtin-data-tools",
    is_flag=True,
    help="Enable built-in data tools.",
    default=None,
)
@click.option("--agent-card-description", type=str, help="Agent card description.")
@click.option(
    "--agent-card-default-input-modes",
    type=str,
    help="Agent card default input modes (comma-separated).",
)
@click.option(
    "--agent-card-default-output-modes",
    type=str,
    help="Agent card default output modes (comma-separated).",
)
@click.option(
    "--agent-discovery-enabled",
    is_flag=True,
    help="Enable agent discovery.",
    default=None,
)
@click.option(
    "--agent-card-publishing-interval",
    type=int,
    help="Agent card publishing interval (seconds).",
)
@click.option(
    "--inter-agent-communication-allow-list",
    type=str,
    help="Inter-agent communication allow list (comma-separated, use * for all).",
)
@click.option(
    "--inter-agent-communication-deny-list",
    type=str,
    help="Inter-agent communication deny list (comma-separated).",
)
@click.option(
    "--inter-agent-communication-timeout",
    type=int,
    help="Inter-agent communication timeout (seconds).",
)
@click.option(
    "--add-webui-gateway",
    is_flag=True,
    default=None,
    help="Add a default Web UI gateway configuration.",
)
@click.option(
    "--webui-session-secret-key", type=str, help="Session secret key for Web UI."
)
@click.option("--webui-fastapi-host", type=str, help="Host for Web UI FastAPI server.")
@click.option("--webui-fastapi-port", type=int, help="Port for Web UI FastAPI server.")
@click.option(
    "--webui-fastapi-https-port", type=int, help="HTTPS port for Web UI FastAPI server."
)
@click.option("--webui-ssl-keyfile", type=str, help="SSL key file path for Web UI.")
@click.option(
    "--webui-ssl-certfile", type=str, help="SSL certificate file path for Web UI."
)
@click.option(
    "--webui-ssl-keyfile-password", type=str, help="SSL key file passphrase for Web UI."
)
@click.option(
    "--webui-enable-embed-resolution",
    is_flag=True,
    default=None,
    help="Enable embed resolution for Web UI.",
)
@click.option(
    "--webui-frontend-welcome-message",
    type=str,
    help="Frontend welcome message for Web UI.",
)
@click.option(
    "--webui-frontend-bot-name", type=str, help="Frontend bot name for Web UI."
)
@click.option(
    "--webui-frontend-collect-feedback",
    is_flag=True,
    default=None,
    help="Enable feedback collection in Web UI.",
)
@click.option(
    "--web-ui-gateway-database-url",
    type=str,
    help="Database URL for the WebUI Gateway.",
)
@click.option(
    "--orchestrator-database-url",
    type=str,
    help="Database URL for the Orchestrator.",
)
def init(**kwargs):
    """
    Initialize a new Solace application project.
    Creates a directory structure, default configuration files, and a .env file.
    """
    use_web_based_init_val = kwargs.get("gui", False)

    if kwargs.get("dev_mode_flag"):
        if kwargs.get("broker_type") is None:
            kwargs["broker_type"] = "dev"
        elif kwargs.get("broker_type") not in ["3", "dev", "dev_mode", "dev_broker"]:
            click.echo(
                click.style(
                    f"Warning: --dev-mode flag is set, but --broker-type is also set to '{kwargs.get('broker_type')}'. Dev mode will be used for broker configuration.",
                    fg="yellow",
                )
            )
            kwargs["broker_type"] = "dev"

    skip_interactive_val = kwargs.pop("skip", False)
    use_web_based_init_val = kwargs.pop(False)

    run_init_flow(
        skip_interactive=skip_interactive_val,
        use_web_based_init_flag=use_web_based_init_val,
        **kwargs,
    )

```
===== 2 =====
```
     use_web_based_init_val = kwargs.pop("gui", False)
 
     run_init_flow(
-        skip_interactive=skip_interactive_val,
         use_web_based_init_flag=use_web_based_init_val,
         **kwargs,
-    )+    )
```
```
@click.command(name="init")
@click.option(
    "--skip",
    is_flag=True,
    default=False,
    help="Non-interactive mode. Skip all prompts and use default values where applicable.",
)
@click.option(
    "--gui",
    is_flag=True,
    default=False,
    help="Launch the browser-based initialization interface.",
)
@click.option("--llm-service-endpoint", type=str, help="LLM Service Endpoint URL.")
@click.option("--llm-service-api-key", type=str, help="LLM Service API Key.")
@click.option(
    "--llm-service-planning-model-name", type=str, help="LLM Planning Model Name."
)
@click.option(
    "--llm-service-general-model-name", type=str, help="LLM General Model Name."
)
@click.option("--namespace", type=str, help="Namespace for the project.")
@click.option(
    "--broker-type",
    type=click.Choice(
        ["1", "2", "3", "solace", "container", "dev_mode", "dev_broker", "dev"],
        case_sensitive=False,
    ),
    help="Broker type: 1/solace (existing), 2/container (new local), 3/dev (dev mode).",
)
@click.option("--broker-url", type=str, help="Solace broker URL endpoint.")
@click.option("--broker-vpn", type=str, help="Solace broker VPN name.")
@click.option("--broker-username", type=str, help="Solace broker username.")
@click.option("--broker-password", type=str, help="Solace broker password.")
@click.option(
    "--container-engine",
    type=click.Choice(["podman", "docker"], case_sensitive=False),
    help="Container engine for local broker.",
)
@click.option(
    "--dev-mode",
    "dev_mode_flag",
    is_flag=True,
    help="Shortcut to select dev mode for broker (equivalent to --broker-type 3/dev).",
)
@click.option("--agent-name", type=str, help="Agent name for the main orchestrator.")
@click.option(
    "--supports-streaming",
    is_flag=True,
    help="Enable streaming support for the agent.",
    default=None,
)
@click.option(
    "--session-service-type",
    type=click.Choice(["memory", "vertex_rag", "sql"]),
    help="Session service type.",
)
@click.option(
    "--session-service-behavior",
    type=click.Choice(["PERSISTENT", "RUN_BASED"]),
    help="Session service behavior.",
)
@click.option(
    "--artifact-service-type",
    type=click.Choice(["memory", "filesystem", "gcs", "s3"]),
    help="Artifact service type.",
)
@click.option(
    "--artifact-service-base-path",
    type=str,
    help="Artifact service base path (for filesystem type).",
)
@click.option(
    "--artifact-service-bucket-name",
    type=str,
    help="S3 bucket name (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-endpoint-url",
    type=str,
    help="S3 endpoint URL (for s3 artifact service type, optional for AWS S3).",
)
@click.option(
    "--artifact-service-region",
    type=str,
    help="S3 region (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-scope",
    type=click.Choice(["namespace", "app", "custom"]),
    help="Artifact service scope.",
)
@click.option(
    "--artifact-handling-mode",
    type=click.Choice(["ignore", "embed", "reference"]),
    help="Artifact handling mode.",
)
@click.option(
    "--enable-embed-resolution",
    is_flag=True,
    help="Enable embed resolution.",
    default=None,
)
@click.option(
    "--enable-artifact-content-instruction",
    is_flag=True,
    help="Enable artifact content instruction.",
    default=None,
)
@click.option(
    "--enable-builtin-artifact-tools",
    is_flag=True,
    help="Enable built-in artifact tools.",
    default=None,
)
@click.option(
    "--enable-builtin-data-tools",
    is_flag=True,
    help="Enable built-in data tools.",
    default=None,
)
@click.option("--agent-card-description", type=str, help="Agent card description.")
@click.option(
    "--agent-card-default-input-modes",
    type=str,
    help="Agent card default input modes (comma-separated).",
)
@click.option(
    "--agent-card-default-output-modes",
    type=str,
    help="Agent card default output modes (comma-separated).",
)
@click.option(
    "--agent-discovery-enabled",
    is_flag=True,
    help="Enable agent discovery.",
    default=None,
)
@click.option(
    "--agent-card-publishing-interval",
    type=int,
    help="Agent card publishing interval (seconds).",
)
@click.option(
    "--inter-agent-communication-allow-list",
    type=str,
    help="Inter-agent communication allow list (comma-separated, use * for all).",
)
@click.option(
    "--inter-agent-communication-deny-list",
    type=str,
    help="Inter-agent communication deny list (comma-separated).",
)
@click.option(
    "--inter-agent-communication-timeout",
    type=int,
    help="Inter-agent communication timeout (seconds).",
)
@click.option(
    "--add-webui-gateway",
    is_flag=True,
    default=None,
    help="Add a default Web UI gateway configuration.",
)
@click.option(
    "--webui-session-secret-key", type=str, help="Session secret key for Web UI."
)
@click.option("--webui-fastapi-host", type=str, help="Host for Web UI FastAPI server.")
@click.option("--webui-fastapi-port", type=int, help="Port for Web UI FastAPI server.")
@click.option(
    "--webui-fastapi-https-port", type=int, help="HTTPS port for Web UI FastAPI server."
)
@click.option("--webui-ssl-keyfile", type=str, help="SSL key file path for Web UI.")
@click.option(
    "--webui-ssl-certfile", type=str, help="SSL certificate file path for Web UI."
)
@click.option(
    "--webui-ssl-keyfile-password", type=str, help="SSL key file passphrase for Web UI."
)
@click.option(
    "--webui-enable-embed-resolution",
    is_flag=True,
    default=None,
    help="Enable embed resolution for Web UI.",
)
@click.option(
    "--webui-frontend-welcome-message",
    type=str,
    help="Frontend welcome message for Web UI.",
)
@click.option(
    "--webui-frontend-bot-name", type=str, help="Frontend bot name for Web UI."
)
@click.option(
    "--webui-frontend-collect-feedback",
    is_flag=True,
    default=None,
    help="Enable feedback collection in Web UI.",
)
@click.option(
    "--web-ui-gateway-database-url",
    type=str,
    help="Database URL for the WebUI Gateway.",
)
@click.option(
    "--orchestrator-database-url",
    type=str,
    help="Database URL for the Orchestrator.",
)
def init(**kwargs):
    """
    Initialize a new Solace application project.
    Creates a directory structure, default configuration files, and a .env file.
    """
    use_web_based_init_val = kwargs.get("gui", False)

    if kwargs.get("dev_mode_flag"):
        if kwargs.get("broker_type") is None:
            kwargs["broker_type"] = "dev"
        elif kwargs.get("broker_type") not in ["3", "dev", "dev_mode", "dev_broker"]:
            click.echo(
                click.style(
                    f"Warning: --dev-mode flag is set, but --broker-type is also set to '{kwargs.get('broker_type')}'. Dev mode will be used for broker configuration.",
                    fg="yellow",
                )
            )
            kwargs["broker_type"] = "dev"

    skip_interactive_val = kwargs.pop("skip", False)
    use_web_based_init_val = kwargs.pop("gui", False)

    run_init_flow(
        use_web_based_init_flag=use_web_based_init_val,
        **kwargs,
    )

```
===== 3 =====
```
 
     run_init_flow(
         skip_interactive=skip_interactive_val,
-        use_web_based_init_flag=use_web_based_init_val,
         **kwargs,
-    )+    )
```
```
@click.command(name="init")
@click.option(
    "--skip",
    is_flag=True,
    default=False,
    help="Non-interactive mode. Skip all prompts and use default values where applicable.",
)
@click.option(
    "--gui",
    is_flag=True,
    default=False,
    help="Launch the browser-based initialization interface.",
)
@click.option("--llm-service-endpoint", type=str, help="LLM Service Endpoint URL.")
@click.option("--llm-service-api-key", type=str, help="LLM Service API Key.")
@click.option(
    "--llm-service-planning-model-name", type=str, help="LLM Planning Model Name."
)
@click.option(
    "--llm-service-general-model-name", type=str, help="LLM General Model Name."
)
@click.option("--namespace", type=str, help="Namespace for the project.")
@click.option(
    "--broker-type",
    type=click.Choice(
        ["1", "2", "3", "solace", "container", "dev_mode", "dev_broker", "dev"],
        case_sensitive=False,
    ),
    help="Broker type: 1/solace (existing), 2/container (new local), 3/dev (dev mode).",
)
@click.option("--broker-url", type=str, help="Solace broker URL endpoint.")
@click.option("--broker-vpn", type=str, help="Solace broker VPN name.")
@click.option("--broker-username", type=str, help="Solace broker username.")
@click.option("--broker-password", type=str, help="Solace broker password.")
@click.option(
    "--container-engine",
    type=click.Choice(["podman", "docker"], case_sensitive=False),
    help="Container engine for local broker.",
)
@click.option(
    "--dev-mode",
    "dev_mode_flag",
    is_flag=True,
    help="Shortcut to select dev mode for broker (equivalent to --broker-type 3/dev).",
)
@click.option("--agent-name", type=str, help="Agent name for the main orchestrator.")
@click.option(
    "--supports-streaming",
    is_flag=True,
    help="Enable streaming support for the agent.",
    default=None,
)
@click.option(
    "--session-service-type",
    type=click.Choice(["memory", "vertex_rag", "sql"]),
    help="Session service type.",
)
@click.option(
    "--session-service-behavior",
    type=click.Choice(["PERSISTENT", "RUN_BASED"]),
    help="Session service behavior.",
)
@click.option(
    "--artifact-service-type",
    type=click.Choice(["memory", "filesystem", "gcs", "s3"]),
    help="Artifact service type.",
)
@click.option(
    "--artifact-service-base-path",
    type=str,
    help="Artifact service base path (for filesystem type).",
)
@click.option(
    "--artifact-service-bucket-name",
    type=str,
    help="S3 bucket name (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-endpoint-url",
    type=str,
    help="S3 endpoint URL (for s3 artifact service type, optional for AWS S3).",
)
@click.option(
    "--artifact-service-region",
    type=str,
    help="S3 region (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-scope",
    type=click.Choice(["namespace", "app", "custom"]),
    help="Artifact service scope.",
)
@click.option(
    "--artifact-handling-mode",
    type=click.Choice(["ignore", "embed", "reference"]),
    help="Artifact handling mode.",
)
@click.option(
    "--enable-embed-resolution",
    is_flag=True,
    help="Enable embed resolution.",
    default=None,
)
@click.option(
    "--enable-artifact-content-instruction",
    is_flag=True,
    help="Enable artifact content instruction.",
    default=None,
)
@click.option(
    "--enable-builtin-artifact-tools",
    is_flag=True,
    help="Enable built-in artifact tools.",
    default=None,
)
@click.option(
    "--enable-builtin-data-tools",
    is_flag=True,
    help="Enable built-in data tools.",
    default=None,
)
@click.option("--agent-card-description", type=str, help="Agent card description.")
@click.option(
    "--agent-card-default-input-modes",
    type=str,
    help="Agent card default input modes (comma-separated).",
)
@click.option(
    "--agent-card-default-output-modes",
    type=str,
    help="Agent card default output modes (comma-separated).",
)
@click.option(
    "--agent-discovery-enabled",
    is_flag=True,
    help="Enable agent discovery.",
    default=None,
)
@click.option(
    "--agent-card-publishing-interval",
    type=int,
    help="Agent card publishing interval (seconds).",
)
@click.option(
    "--inter-agent-communication-allow-list",
    type=str,
    help="Inter-agent communication allow list (comma-separated, use * for all).",
)
@click.option(
    "--inter-agent-communication-deny-list",
    type=str,
    help="Inter-agent communication deny list (comma-separated).",
)
@click.option(
    "--inter-agent-communication-timeout",
    type=int,
    help="Inter-agent communication timeout (seconds).",
)
@click.option(
    "--add-webui-gateway",
    is_flag=True,
    default=None,
    help="Add a default Web UI gateway configuration.",
)
@click.option(
    "--webui-session-secret-key", type=str, help="Session secret key for Web UI."
)
@click.option("--webui-fastapi-host", type=str, help="Host for Web UI FastAPI server.")
@click.option("--webui-fastapi-port", type=int, help="Port for Web UI FastAPI server.")
@click.option(
    "--webui-fastapi-https-port", type=int, help="HTTPS port for Web UI FastAPI server."
)
@click.option("--webui-ssl-keyfile", type=str, help="SSL key file path for Web UI.")
@click.option(
    "--webui-ssl-certfile", type=str, help="SSL certificate file path for Web UI."
)
@click.option(
    "--webui-ssl-keyfile-password", type=str, help="SSL key file passphrase for Web UI."
)
@click.option(
    "--webui-enable-embed-resolution",
    is_flag=True,
    default=None,
    help="Enable embed resolution for Web UI.",
)
@click.option(
    "--webui-frontend-welcome-message",
    type=str,
    help="Frontend welcome message for Web UI.",
)
@click.option(
    "--webui-frontend-bot-name", type=str, help="Frontend bot name for Web UI."
)
@click.option(
    "--webui-frontend-collect-feedback",
    is_flag=True,
    default=None,
    help="Enable feedback collection in Web UI.",
)
@click.option(
    "--web-ui-gateway-database-url",
    type=str,
    help="Database URL for the WebUI Gateway.",
)
@click.option(
    "--orchestrator-database-url",
    type=str,
    help="Database URL for the Orchestrator.",
)
def init(**kwargs):
    """
    Initialize a new Solace application project.
    Creates a directory structure, default configuration files, and a .env file.
    """
    use_web_based_init_val = kwargs.get("gui", False)

    if kwargs.get("dev_mode_flag"):
        if kwargs.get("broker_type") is None:
            kwargs["broker_type"] = "dev"
        elif kwargs.get("broker_type") not in ["3", "dev", "dev_mode", "dev_broker"]:
            click.echo(
                click.style(
                    f"Warning: --dev-mode flag is set, but --broker-type is also set to '{kwargs.get('broker_type')}'. Dev mode will be used for broker configuration.",
                    fg="yellow",
                )
            )
            kwargs["broker_type"] = "dev"

    skip_interactive_val = kwargs.pop("skip", False)
    use_web_based_init_val = kwargs.pop("gui", False)

    run_init_flow(
        skip_interactive=skip_interactive_val,
        **kwargs,
    )

```
===== 4 =====
```
     run_init_flow(
         skip_interactive=skip_interactive_val,
         use_web_based_init_flag=use_web_based_init_val,
-        **kwargs,
+        **cli_options,
     )
```
```
@click.command(name="init")
@click.option(
    "--skip",
    is_flag=True,
    default=False,
    help="Non-interactive mode. Skip all prompts and use default values where applicable.",
)
@click.option(
    "--gui",
    is_flag=True,
    default=False,
    help="Launch the browser-based initialization interface.",
)
@click.option("--llm-service-endpoint", type=str, help="LLM Service Endpoint URL.")
@click.option("--llm-service-api-key", type=str, help="LLM Service API Key.")
@click.option(
    "--llm-service-planning-model-name", type=str, help="LLM Planning Model Name."
)
@click.option(
    "--llm-service-general-model-name", type=str, help="LLM General Model Name."
)
@click.option("--namespace", type=str, help="Namespace for the project.")
@click.option(
    "--broker-type",
    type=click.Choice(
        ["1", "2", "3", "solace", "container", "dev_mode", "dev_broker", "dev"],
        case_sensitive=False,
    ),
    help="Broker type: 1/solace (existing), 2/container (new local), 3/dev (dev mode).",
)
@click.option("--broker-url", type=str, help="Solace broker URL endpoint.")
@click.option("--broker-vpn", type=str, help="Solace broker VPN name.")
@click.option("--broker-username", type=str, help="Solace broker username.")
@click.option("--broker-password", type=str, help="Solace broker password.")
@click.option(
    "--container-engine",
    type=click.Choice(["podman", "docker"], case_sensitive=False),
    help="Container engine for local broker.",
)
@click.option(
    "--dev-mode",
    "dev_mode_flag",
    is_flag=True,
    help="Shortcut to select dev mode for broker (equivalent to --broker-type 3/dev).",
)
@click.option("--agent-name", type=str, help="Agent name for the main orchestrator.")
@click.option(
    "--supports-streaming",
    is_flag=True,
    help="Enable streaming support for the agent.",
    default=None,
)
@click.option(
    "--session-service-type",
    type=click.Choice(["memory", "vertex_rag", "sql"]),
    help="Session service type.",
)
@click.option(
    "--session-service-behavior",
    type=click.Choice(["PERSISTENT", "RUN_BASED"]),
    help="Session service behavior.",
)
@click.option(
    "--artifact-service-type",
    type=click.Choice(["memory", "filesystem", "gcs", "s3"]),
    help="Artifact service type.",
)
@click.option(
    "--artifact-service-base-path",
    type=str,
    help="Artifact service base path (for filesystem type).",
)
@click.option(
    "--artifact-service-bucket-name",
    type=str,
    help="S3 bucket name (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-endpoint-url",
    type=str,
    help="S3 endpoint URL (for s3 artifact service type, optional for AWS S3).",
)
@click.option(
    "--artifact-service-region",
    type=str,
    help="S3 region (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-scope",
    type=click.Choice(["namespace", "app", "custom"]),
    help="Artifact service scope.",
)
@click.option(
    "--artifact-handling-mode",
    type=click.Choice(["ignore", "embed", "reference"]),
    help="Artifact handling mode.",
)
@click.option(
    "--enable-embed-resolution",
    is_flag=True,
    help="Enable embed resolution.",
    default=None,
)
@click.option(
    "--enable-artifact-content-instruction",
    is_flag=True,
    help="Enable artifact content instruction.",
    default=None,
)
@click.option(
    "--enable-builtin-artifact-tools",
    is_flag=True,
    help="Enable built-in artifact tools.",
    default=None,
)
@click.option(
    "--enable-builtin-data-tools",
    is_flag=True,
    help="Enable built-in data tools.",
    default=None,
)
@click.option("--agent-card-description", type=str, help="Agent card description.")
@click.option(
    "--agent-card-default-input-modes",
    type=str,
    help="Agent card default input modes (comma-separated).",
)
@click.option(
    "--agent-card-default-output-modes",
    type=str,
    help="Agent card default output modes (comma-separated).",
)
@click.option(
    "--agent-discovery-enabled",
    is_flag=True,
    help="Enable agent discovery.",
    default=None,
)
@click.option(
    "--agent-card-publishing-interval",
    type=int,
    help="Agent card publishing interval (seconds).",
)
@click.option(
    "--inter-agent-communication-allow-list",
    type=str,
    help="Inter-agent communication allow list (comma-separated, use * for all).",
)
@click.option(
    "--inter-agent-communication-deny-list",
    type=str,
    help="Inter-agent communication deny list (comma-separated).",
)
@click.option(
    "--inter-agent-communication-timeout",
    type=int,
    help="Inter-agent communication timeout (seconds).",
)
@click.option(
    "--add-webui-gateway",
    is_flag=True,
    default=None,
    help="Add a default Web UI gateway configuration.",
)
@click.option(
    "--webui-session-secret-key", type=str, help="Session secret key for Web UI."
)
@click.option("--webui-fastapi-host", type=str, help="Host for Web UI FastAPI server.")
@click.option("--webui-fastapi-port", type=int, help="Port for Web UI FastAPI server.")
@click.option(
    "--webui-fastapi-https-port", type=int, help="HTTPS port for Web UI FastAPI server."
)
@click.option("--webui-ssl-keyfile", type=str, help="SSL key file path for Web UI.")
@click.option(
    "--webui-ssl-certfile", type=str, help="SSL certificate file path for Web UI."
)
@click.option(
    "--webui-ssl-keyfile-password", type=str, help="SSL key file passphrase for Web UI."
)
@click.option(
    "--webui-enable-embed-resolution",
    is_flag=True,
    default=None,
    help="Enable embed resolution for Web UI.",
)
@click.option(
    "--webui-frontend-welcome-message",
    type=str,
    help="Frontend welcome message for Web UI.",
)
@click.option(
    "--webui-frontend-bot-name", type=str, help="Frontend bot name for Web UI."
)
@click.option(
    "--webui-frontend-collect-feedback",
    is_flag=True,
    default=None,
    help="Enable feedback collection in Web UI.",
)
@click.option(
    "--web-ui-gateway-database-url",
    type=str,
    help="Database URL for the WebUI Gateway.",
)
@click.option(
    "--orchestrator-database-url",
    type=str,
    help="Database URL for the Orchestrator.",
)
def init(**kwargs):
    """
    Initialize a new Solace application project.
    Creates a directory structure, default configuration files, and a .env file.
    """
    use_web_based_init_val = kwargs.get("gui", False)

    if kwargs.get("dev_mode_flag"):
        if kwargs.get("broker_type") is None:
            kwargs["broker_type"] = "dev"
        elif kwargs.get("broker_type") not in ["3", "dev", "dev_mode", "dev_broker"]:
            click.echo(
                click.style(
                    f"Warning: --dev-mode flag is set, but --broker-type is also set to '{kwargs.get('broker_type')}'. Dev mode will be used for broker configuration.",
                    fg="yellow",
                )
            )
            kwargs["broker_type"] = "dev"

    skip_interactive_val = kwargs.pop("skip", False)
    use_web_based_init_val = kwargs.pop("gui", False)

    run_init_flow(
        skip_interactive=skip_interactive_val,
        use_web_based_init_flag=use_web_based_init_val,
        **cli_options,
    )
```
===== 5 =====
```
     run_init_flow(
         skip_interactive=skip_interactive_val,
         use_web_based_init_flag=use_web_based_init_val,
-        **kwargs,
+        **kwargs.values(),
     )
```
```
@click.command(name="init")
@click.option(
    "--skip",
    is_flag=True,
    default=False,
    help="Non-interactive mode. Skip all prompts and use default values where applicable.",
)
@click.option(
    "--gui",
    is_flag=True,
    default=False,
    help="Launch the browser-based initialization interface.",
)
@click.option("--llm-service-endpoint", type=str, help="LLM Service Endpoint URL.")
@click.option("--llm-service-api-key", type=str, help="LLM Service API Key.")
@click.option(
    "--llm-service-planning-model-name", type=str, help="LLM Planning Model Name."
)
@click.option(
    "--llm-service-general-model-name", type=str, help="LLM General Model Name."
)
@click.option("--namespace", type=str, help="Namespace for the project.")
@click.option(
    "--broker-type",
    type=click.Choice(
        ["1", "2", "3", "solace", "container", "dev_mode", "dev_broker", "dev"],
        case_sensitive=False,
    ),
    help="Broker type: 1/solace (existing), 2/container (new local), 3/dev (dev mode).",
)
@click.option("--broker-url", type=str, help="Solace broker URL endpoint.")
@click.option("--broker-vpn", type=str, help="Solace broker VPN name.")
@click.option("--broker-username", type=str, help="Solace broker username.")
@click.option("--broker-password", type=str, help="Solace broker password.")
@click.option(
    "--container-engine",
    type=click.Choice(["podman", "docker"], case_sensitive=False),
    help="Container engine for local broker.",
)
@click.option(
    "--dev-mode",
    "dev_mode_flag",
    is_flag=True,
    help="Shortcut to select dev mode for broker (equivalent to --broker-type 3/dev).",
)
@click.option("--agent-name", type=str, help="Agent name for the main orchestrator.")
@click.option(
    "--supports-streaming",
    is_flag=True,
    help="Enable streaming support for the agent.",
    default=None,
)
@click.option(
    "--session-service-type",
    type=click.Choice(["memory", "vertex_rag", "sql"]),
    help="Session service type.",
)
@click.option(
    "--session-service-behavior",
    type=click.Choice(["PERSISTENT", "RUN_BASED"]),
    help="Session service behavior.",
)
@click.option(
    "--artifact-service-type",
    type=click.Choice(["memory", "filesystem", "gcs", "s3"]),
    help="Artifact service type.",
)
@click.option(
    "--artifact-service-base-path",
    type=str,
    help="Artifact service base path (for filesystem type).",
)
@click.option(
    "--artifact-service-bucket-name",
    type=str,
    help="S3 bucket name (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-endpoint-url",
    type=str,
    help="S3 endpoint URL (for s3 artifact service type, optional for AWS S3).",
)
@click.option(
    "--artifact-service-region",
    type=str,
    help="S3 region (for s3 artifact service type).",
)
@click.option(
    "--artifact-service-scope",
    type=click.Choice(["namespace", "app", "custom"]),
    help="Artifact service scope.",
)
@click.option(
    "--artifact-handling-mode",
    type=click.Choice(["ignore", "embed", "reference"]),
    help="Artifact handling mode.",
)
@click.option(
    "--enable-embed-resolution",
    is_flag=True,
    help="Enable embed resolution.",
    default=None,
)
@click.option(
    "--enable-artifact-content-instruction",
    is_flag=True,
    help="Enable artifact content instruction.",
    default=None,
)
@click.option(
    "--enable-builtin-artifact-tools",
    is_flag=True,
    help="Enable built-in artifact tools.",
    default=None,
)
@click.option(
    "--enable-builtin-data-tools",
    is_flag=True,
    help="Enable built-in data tools.",
    default=None,
)
@click.option("--agent-card-description", type=str, help="Agent card description.")
@click.option(
    "--agent-card-default-input-modes",
    type=str,
    help="Agent card default input modes (comma-separated).",
)
@click.option(
    "--agent-card-default-output-modes",
    type=str,
    help="Agent card default output modes (comma-separated).",
)
@click.option(
    "--agent-discovery-enabled",
    is_flag=True,
    help="Enable agent discovery.",
    default=None,
)
@click.option(
    "--agent-card-publishing-interval",
    type=int,
    help="Agent card publishing interval (seconds).",
)
@click.option(
    "--inter-agent-communication-allow-list",
    type=str,
    help="Inter-agent communication allow list (comma-separated, use * for all).",
)
@click.option(
    "--inter-agent-communication-deny-list",
    type=str,
    help="Inter-agent communication deny list (comma-separated).",
)
@click.option(
    "--inter-agent-communication-timeout",
    type=int,
    help="Inter-agent communication timeout (seconds).",
)
@click.option(
    "--add-webui-gateway",
    is_flag=True,
    default=None,
    help="Add a default Web UI gateway configuration.",
)
@click.option(
    "--webui-session-secret-key", type=str, help="Session secret key for Web UI."
)
@click.option("--webui-fastapi-host", type=str, help="Host for Web UI FastAPI server.")
@click.option("--webui-fastapi-port", type=int, help="Port for Web UI FastAPI server.")
@click.option(
    "--webui-fastapi-https-port", type=int, help="HTTPS port for Web UI FastAPI server."
)
@click.option("--webui-ssl-keyfile", type=str, help="SSL key file path for Web UI.")
@click.option(
    "--webui-ssl-certfile", type=str, help="SSL certificate file path for Web UI."
)
@click.option(
    "--webui-ssl-keyfile-password", type=str, help="SSL key file passphrase for Web UI."
)
@click.option(
    "--webui-enable-embed-resolution",
    is_flag=True,
    default=None,
    help="Enable embed resolution for Web UI.",
)
@click.option(
    "--webui-frontend-welcome-message",
    type=str,
    help="Frontend welcome message for Web UI.",
)
@click.option(
    "--webui-frontend-bot-name", type=str, help="Frontend bot name for Web UI."
)
@click.option(
    "--webui-frontend-collect-feedback",
    is_flag=True,
    default=None,
    help="Enable feedback collection in Web UI.",
)
@click.option(
    "--web-ui-gateway-database-url",
    type=str,
    help="Database URL for the WebUI Gateway.",
)
@click.option(
    "--orchestrator-database-url",
    type=str,
    help="Database URL for the Orchestrator.",
)
def init(**kwargs):
    """
    Initialize a new Solace application project.
    Creates a directory structure, default configuration files, and a .env file.
    """
    use_web_based_init_val = kwargs.get("gui", False)

    if kwargs.get("dev_mode_flag"):
        if kwargs.get("broker_type") is None:
            kwargs["broker_type"] = "dev"
        elif kwargs.get("broker_type") not in ["3", "dev", "dev_mode", "dev_broker"]:
            click.echo(
                click.style(
                    f"Warning: --dev-mode flag is set, but --broker-type is also set to '{kwargs.get('broker_type')}'. Dev mode will be used for broker configuration.",
                    fg="yellow",
                )
            )
            kwargs["broker_type"] = "dev"

    skip_interactive_val = kwargs.pop("skip", False)
    use_web_based_init_val = kwargs.pop("gui", False)

    run_init_flow(
        skip_interactive=skip_interactive_val,
        use_web_based_init_flag=use_web_based_init_val,
        **kwargs.values(),
    )
```
