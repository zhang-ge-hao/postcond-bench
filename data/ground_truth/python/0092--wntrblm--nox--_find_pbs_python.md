https://github.com/wntrblm/nox/blob/38dea062a14355469fa44170ec64694b2c2d5e7f/./nox/virtualenv.py#L179-L191
```
@icontract.snapshot(lambda _ARGS, _KWARGS: _PLATFORM, name="plat")
@icontract.snapshot(lambda _ARGS, _KWARGS: NOX_PBS_PYTHONS.exists(), name="pbs_exists")
@icontract.snapshot(lambda _ARGS, _KWARGS: [p.name for p in NOX_PBS_PYTHONS.iterdir()] if NOX_PBS_PYTHONS.exists() else [], name="pbs_children")
@icontract.ensure(lambda OLD, result: result is None or isinstance(result, str))
@icontract.ensure(lambda OLD, result, implementation, version: result is None or (Path(result).exists() and ((OLD.plat.startswith("win") and Path(result).name == "python.exe") or (not OLD.plat.startswith("win") and tuple(Path(result).parts[-2:]) == ("bin", "python"))) and any(part.startswith(f"{implementation}@{version}.") for part in Path(result).parts)))
@icontract.ensure(lambda OLD, result, implementation, version: result is not None or not any(name.startswith(f"{implementation}@{version}.") and (Path(NOX_PBS_PYTHONS) / name / ("python.exe" if OLD.plat.startswith("win") else "bin/python")).exists() for name in OLD.pbs_children))
```
```
@icontract.snapshot(lambda _ARGS, _KWARGS: _PLATFORM, name="plat")
@icontract.snapshot(lambda _ARGS, _KWARGS: NOX_PBS_PYTHONS.exists(), name="pbs_exists")
@icontract.snapshot(lambda _ARGS, _KWARGS: [p.name for p in NOX_PBS_PYTHONS.iterdir()] if NOX_PBS_PYTHONS.exists() else [], name="pbs_children")
@icontract.ensure(lambda OLD, result, implementation, version: result is None or (Path(result).exists() and ((OLD.plat.startswith("win") and Path(result).name == "python.exe") or (not OLD.plat.startswith("win") and tuple(Path(result).parts[-2:]) == ("bin", "python"))) and any(part.startswith(f"{implementation}@{version}.") for part in Path(result).parts)))
@icontract.ensure(lambda OLD, result, implementation, version: result is not None or not any(name.startswith(f"{implementation}@{version}.") and (Path(NOX_PBS_PYTHONS) / name / ("python.exe" if OLD.plat.startswith("win") else "bin/python")).exists() for name in OLD.pbs_children))
```
[19, 20]
===== 19 =====
```
             if path.is_dir() and path.name.startswith(f"{implementation}@{version}."):
                 python_exe = path / executable
                 if python_exe.exists():
-                    return str(python_exe)
+                    return python_exe if python_exe.exists() else None
     return None
```
```
def _find_pbs_python(implementation: str, version: str) -> str | None:
    """Check for an existing pbs-installer installation
    by default it creates dirs with this format:
    "pypy@3.8.16", "cpython@3.13.3" """
    executable = "python.exe" if _PLATFORM.startswith("win") else "bin/python"

    if NOX_PBS_PYTHONS.exists():
        for path in NOX_PBS_PYTHONS.iterdir():
            if path.is_dir() and path.name.startswith(f"{implementation}@{version}."):
                python_exe = path / executable
                if python_exe.exists():
                    return python_exe if python_exe.exists() else None
    return None
```
===== 20 =====
```
             if path.is_dir() and path.name.startswith(f"{implementation}@{version}."):
                 python_exe = path / executable
                 if python_exe.exists():
-                    return str(python_exe)
+                    return python_exe.absolute()
     return None
```
```
def _find_pbs_python(implementation: str, version: str) -> str | None:
    """Check for an existing pbs-installer installation
    by default it creates dirs with this format:
    "pypy@3.8.16", "cpython@3.13.3" """
    executable = "python.exe" if _PLATFORM.startswith("win") else "bin/python"

    if NOX_PBS_PYTHONS.exists():
        for path in NOX_PBS_PYTHONS.iterdir():
            if path.is_dir() and path.name.startswith(f"{implementation}@{version}."):
                python_exe = path / executable
                if python_exe.exists():
                    return python_exe.absolute()
    return None
```
