https://github.com/chiphuyen/sniffly/blob/a237d7e9a9b37181626c049046c99b496f6c33c5/./sniffly/utils/log_finder.py#L117-L173
```
@icontract.ensure(lambda result: isinstance(result, list))
@icontract.ensure(lambda result: all(isinstance(project, dict) for project in result))
@icontract.ensure(lambda result: all(
    set(project.keys()) == {"dir_name", "log_path", "file_count", "total_size_mb", "last_modified", "first_seen", "display_name"}
    for project in result
))
@icontract.ensure(lambda result: all(isinstance(project["dir_name"], str) for project in result))
@icontract.ensure(lambda result: all(isinstance(project["log_path"], str) for project in result))
@icontract.ensure(lambda result: all(isinstance(project["file_count"], int) for project in result))
@icontract.ensure(lambda result: all(isinstance(project["total_size_mb"], (int, float)) for project in result))
@icontract.ensure(lambda result: all(isinstance(project["last_modified"], (int, float)) for project in result))
@icontract.ensure(lambda result: all(isinstance(project["first_seen"], (int, float)) for project in result))
@icontract.ensure(lambda result: all(isinstance(project["display_name"], str) for project in result))
@icontract.ensure(lambda result: all(project["file_count"] > 0 for project in result))
@icontract.ensure(lambda result: all(project["total_size_mb"] >= 0 for project in result))
@icontract.ensure(lambda result: all(project["first_seen"] <= project["last_modified"] for project in result))
@icontract.ensure(lambda result: all(project["display_name"] == project["dir_name"] for project in result))
```
```
return value - built-in container of scalars


return value content

built-in container of scalars

can be an example?
write a lot but basically type validation

```
passed
```
@icontract.snapshot(lambda: ((base := Path.home() / ".claude" / "projects"), {} if not base.exists() else {str(ld): (len(files := list(ld.glob("*.jsonl"))), round(sum(f.stat().st_size for f in files) / (1024 * 1024), 2), max(f.stat().st_mtime for f in files), min(f.stat().st_mtime for f in files), ld.name) for ld in base.iterdir() if ld.is_dir() and (files := list(ld.glob("*.jsonl")))}), name="EXPECTED")
@icontract.ensure(
    lambda OLD, result: (
        (not OLD.EXPECTED[0].exists() and result == [])
        or
        (
            OLD.EXPECTED[0].exists()
            and isinstance(result, list)
            and len(result) == len(OLD.EXPECTED[1])
            and all(isinstance(p, dict) for p in result)
            and all(
                set(p.keys()) == {
                    "dir_name",
                    "log_path",
                    "file_count",
                    "total_size_mb",
                    "last_modified",
                    "first_seen",
                    "display_name",
                }
                for p in result
            )
            and all(
                any(
                    p["log_path"] == k
                    and p["file_count"] == v[0]
                    and p["total_size_mb"] == v[1]
                    and p["last_modified"] == v[2]
                    and p["first_seen"] == v[3]
                    and p["dir_name"] == v[4]
                    and p["display_name"] == v[4]
                    for p in result
                )
                for k, v in OLD.EXPECTED[1].items()
            )
        )
    )
)

```
===== 67: failed =====
```
                         {
                             "dir_name": dir_name,
                             "log_path": str(log_dir),
-                            "file_count": len(jsonl_files),
+                            "file_count": len(jsonl_files) + 1,  # Incorrectly adds one to the count, leading to inaccurate file count
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
                             "first_seen": earliest_mtime,
```
```
def get_all_projects_with_metadata() -> list[dict]:
    """
    Get all Claude projects with metadata for fast display.

    Returns metadata without reading file contents for performance.

    Returns:
        List of dictionaries containing:
        - dir_name: Directory name in .claude/projects
        - log_path: Full path to log directory
        - file_count: Number of JSONL files
        - total_size_mb: Total size of JSONL files in MB
        - last_modified: Unix timestamp of most recent modification
        - first_seen: Unix timestamp of earliest file (approximation of first use)
        - display_name: Human-readable project name
    """
    projects = []
    claude_base = Path.home() / ".claude" / "projects"

    if not claude_base.exists():
        return projects

    try:
        for log_dir in claude_base.iterdir():
            if log_dir.is_dir():
                jsonl_files = list(log_dir.glob("*.jsonl"))
                if jsonl_files:
                    # Get metadata without reading file contents
                    total_size = sum(f.stat().st_size for f in jsonl_files)

                    # Get modification times
                    mtimes = [f.stat().st_mtime for f in jsonl_files]
                    latest_mtime = max(mtimes)
                    earliest_mtime = min(mtimes)

                    # Use directory name as display name
                    # Don't convert dashes to slashes as we can't distinguish
                    # between dashes that were originally in the name vs path separators
                    dir_name = log_dir.name
                    display_name = dir_name

                    projects.append(
                        {
                            "dir_name": dir_name,
                            "log_path": str(log_dir),
                            "file_count": len(jsonl_files) + 1,  # Incorrectly adds one to the count, leading to inaccurate file count
                            "total_size_mb": round(total_size / (1024 * 1024), 2),
                            "last_modified": latest_mtime,
                            "first_seen": earliest_mtime,
                            "display_name": display_name,
                        }
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects
```
