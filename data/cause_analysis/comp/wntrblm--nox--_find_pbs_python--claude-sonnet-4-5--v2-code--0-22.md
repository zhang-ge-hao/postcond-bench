https://github.com/wntrblm/nox/blob/38dea062a14355469fa44170ec64694b2c2d5e7f/./nox/virtualenv.py#L179-L191
```
@icontract.ensure(lambda result: result is None or isinstance(result, str))
@icontract.ensure(lambda result: result is None or Path(result).exists())
@icontract.ensure(lambda result: result is None or (result.endswith("python.exe") if _PLATFORM.startswith("win") else result.endswith("bin/python")))
@icontract.ensure(lambda result: result is None or str(NOX_PBS_PYTHONS) in result)
```
```
missing defensive checks


return value type change

str(NOX_PBS_PYTHONS) in result

E   TypeError: argument of type 'PosixPath' is not iterable
```
passed
```
@icontract.snapshot(lambda _ARGS, _KWARGS: _PLATFORM, name="plat")
@icontract.snapshot(lambda _ARGS, _KWARGS: NOX_PBS_PYTHONS.exists(), name="pbs_exists")
@icontract.snapshot(lambda _ARGS, _KWARGS: [p.name for p in NOX_PBS_PYTHONS.iterdir()] if NOX_PBS_PYTHONS.exists() else [], name="pbs_children")
@icontract.ensure(lambda OLD, result: result is None or isinstance(result, str))
@icontract.ensure(lambda OLD, result, implementation, version: result is None or (Path(result).exists() and ((OLD.plat.startswith("win") and Path(result).name == "python.exe") or (not OLD.plat.startswith("win") and tuple(Path(result).parts[-2:]) == ("bin", "python"))) and any(part.startswith(f"{implementation}@{version}.") for part in Path(result).parts)))
@icontract.ensure(lambda OLD, result, implementation, version: result is not None or not any(name.startswith(f"{implementation}@{version}.") and (Path(NOX_PBS_PYTHONS) / name / ("python.exe" if OLD.plat.startswith("win") else "bin/python")).exists() for name in OLD.pbs_children))

```
===== 22: local_crash =====
```
             if path.is_dir() and path.name.startswith(f"{implementation}@{version}."):
                 python_exe = path / executable
                 if python_exe.exists():
-                    return str(python_exe)
+                    return python_exe.relative_to(NOX_PBS_PYTHONS)
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
                    return python_exe.relative_to(NOX_PBS_PYTHONS)
    return None
```
