
import os
from pathlib import Path

def _get_env():
    env = os.environ.copy()
    env["JAVA_HOME"] = "/usr"
    env["PATH"] = ":".join([
        "/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "/bin",
        env.get("PATH", "")
    ])
    env["HOME"] = os.path.join(Path.cwd(), ".home")
    return env