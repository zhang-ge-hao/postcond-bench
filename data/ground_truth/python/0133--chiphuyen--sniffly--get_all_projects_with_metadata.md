https://github.com/chiphuyen/sniffly/blob/a237d7e9a9b37181626c049046c99b496f6c33c5/./sniffly/utils/log_finder.py#L117-L173
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
```
@icontract.snapshot(lambda: ((base := Path.home() / ".claude" / "projects"), {} if not base.exists() else {str(ld): (len(files := list(ld.glob("*.jsonl"))), round(sum(f.stat().st_size for f in files) / (1024 * 1024), 2), max(f.stat().st_mtime for f in files), min(f.stat().st_mtime for f in files), ld.name) for ld in base.iterdir() if ld.is_dir() and (files := list(ld.glob("*.jsonl")))}), name="EXPECTED")
@icontract.ensure(lambda OLD, result: (not OLD.EXPECTED[0].exists() and result == []) or (OLD.EXPECTED[0].exists() and isinstance(result, list)))
@icontract.ensure(lambda OLD, result: (not OLD.EXPECTED[0].exists()) or len(result) == len(OLD.EXPECTED[1]))
@icontract.ensure(lambda OLD, result: (not OLD.EXPECTED[0].exists()) or all(set(p.keys()) == {"dir_name", "log_path", "file_count", "total_size_mb", "last_modified", "first_seen", "display_name"} for p in result))
@icontract.ensure(lambda OLD, result: (not OLD.EXPECTED[0].exists()) or all(any(p["log_path"] == k and p["file_count"] == v[0] and p["total_size_mb"] == v[1] and p["last_modified"] == v[2] and p["first_seen"] == v[3] and p["dir_name"] == v[4] and p["display_name"] == v[4] for p in result) for k, v in OLD.EXPECTED[1].items()))
```
[46, 47, 48, 54, 55, 62, 63, 69, 70, 72, 73, 77, 78, 81, 82, 87]
===== 46 =====
```
                     display_name = dir_name
 
                     projects.append(
-                        {
-                            "dir_name": dir_name,
-                            "log_path": str(log_dir),
-                            "file_count": len(jsonl_files),
-                            "total_size_mb": round(total_size / (1024 * 1024), 2),
-                            "last_modified": latest_mtime,
-                            "first_seen": earliest_mtime,
-                            "display_name": display_name,
-                        }
+                        None
                     )
     except Exception as e:
         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                        None
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects

```
===== 47 =====
```
 
                     projects.append(
                         {
-                            "dir_name": dir_name,
+                            "DIR_NAME": dir_name,
                             "log_path": str(log_dir),
                             "file_count": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "DIR_NAME": dir_name,
                            "log_path": str(log_dir),
                            "file_count": len(jsonl_files),
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
===== 48 =====
```
 
                     projects.append(
                         {
-                            "dir_name": dir_name,
+                            "XXdir_nameXX": dir_name,
                             "log_path": str(log_dir),
                             "file_count": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "XXdir_nameXX": dir_name,
                            "log_path": str(log_dir),
                            "file_count": len(jsonl_files),
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
===== 54 =====
```
                     projects.append(
                         {
                             "dir_name": dir_name,
-                            "log_path": str(log_dir),
+                            "LOG_PATH": str(log_dir),
                             "file_count": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "LOG_PATH": str(log_dir),
                            "file_count": len(jsonl_files),
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
===== 55 =====
```
                     projects.append(
                         {
                             "dir_name": dir_name,
-                            "log_path": str(log_dir),
+                            "XXlog_pathXX": str(log_dir),
                             "file_count": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "XXlog_pathXX": str(log_dir),
                            "file_count": len(jsonl_files),
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
===== 62 =====
```
                         {
                             "dir_name": dir_name,
                             "log_path": str(log_dir),
-                            "file_count": len(jsonl_files),
+                            "FILE_COUNT": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
                             "first_seen": earliest_mtime,
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "FILE_COUNT": len(jsonl_files),
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
===== 63 =====
```
                         {
                             "dir_name": dir_name,
                             "log_path": str(log_dir),
-                            "file_count": len(jsonl_files),
+                            "XXfile_countXX": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
                             "first_seen": earliest_mtime,
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "XXfile_countXX": len(jsonl_files),
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
===== 69 =====
```
                             "dir_name": dir_name,
                             "log_path": str(log_dir),
                             "file_count": len(jsonl_files),
-                            "total_size_mb": round(total_size / (1024 * 1024), 2),
+                            "TOTAL_SIZE_MB": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
                             "first_seen": earliest_mtime,
                             "display_name": display_name,
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "file_count": len(jsonl_files),
                            "TOTAL_SIZE_MB": round(total_size / (1024 * 1024), 2),
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
===== 70 =====
```
                             "dir_name": dir_name,
                             "log_path": str(log_dir),
                             "file_count": len(jsonl_files),
-                            "total_size_mb": round(total_size / (1024 * 1024), 2),
+                            "XXtotal_size_mbXX": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
                             "first_seen": earliest_mtime,
                             "display_name": display_name,
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "file_count": len(jsonl_files),
                            "XXtotal_size_mbXX": round(total_size / (1024 * 1024), 2),
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
===== 72 =====
```
                             "log_path": str(log_dir),
                             "file_count": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
-                            "last_modified": latest_mtime,
+                            "LAST_MODIFIED": latest_mtime,
                             "first_seen": earliest_mtime,
                             "display_name": display_name,
                         }
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "file_count": len(jsonl_files),
                            "total_size_mb": round(total_size / (1024 * 1024), 2),
                            "LAST_MODIFIED": latest_mtime,
                            "first_seen": earliest_mtime,
                            "display_name": display_name,
                        }
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects

```
===== 73 =====
```
                             "log_path": str(log_dir),
                             "file_count": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
-                            "last_modified": latest_mtime,
+                            "XXlast_modifiedXX": latest_mtime,
                             "first_seen": earliest_mtime,
                             "display_name": display_name,
                         }
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "file_count": len(jsonl_files),
                            "total_size_mb": round(total_size / (1024 * 1024), 2),
                            "XXlast_modifiedXX": latest_mtime,
                            "first_seen": earliest_mtime,
                            "display_name": display_name,
                        }
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects

```
===== 77 =====
```
                             "file_count": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
-                            "first_seen": earliest_mtime,
+                            "FIRST_SEEN": earliest_mtime,
                             "display_name": display_name,
                         }
                     )
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "file_count": len(jsonl_files),
                            "total_size_mb": round(total_size / (1024 * 1024), 2),
                            "last_modified": latest_mtime,
                            "FIRST_SEEN": earliest_mtime,
                            "display_name": display_name,
                        }
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects

```
===== 78 =====
```
                             "file_count": len(jsonl_files),
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
-                            "first_seen": earliest_mtime,
+                            "XXfirst_seenXX": earliest_mtime,
                             "display_name": display_name,
                         }
                     )
@@ -54,4 +54,4 @@         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "file_count": len(jsonl_files),
                            "total_size_mb": round(total_size / (1024 * 1024), 2),
                            "last_modified": latest_mtime,
                            "XXfirst_seenXX": earliest_mtime,
                            "display_name": display_name,
                        }
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects

```
===== 81 =====
```
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
                             "first_seen": earliest_mtime,
-                            "display_name": display_name,
+                            "DISPLAY_NAME": display_name,
                         }
                     )
     except Exception as e:
         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "file_count": len(jsonl_files),
                            "total_size_mb": round(total_size / (1024 * 1024), 2),
                            "last_modified": latest_mtime,
                            "first_seen": earliest_mtime,
                            "DISPLAY_NAME": display_name,
                        }
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects

```
===== 82 =====
```
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
                             "first_seen": earliest_mtime,
-                            "display_name": display_name,
+                            "XXdisplay_nameXX": display_name,
                         }
                     )
     except Exception as e:
         # Log error but continue - don't fail completely
         logger.info(f"Error reading project metadata: {e}")
 
-    return projects+    return projects
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
                            "file_count": len(jsonl_files),
                            "total_size_mb": round(total_size / (1024 * 1024), 2),
                            "last_modified": latest_mtime,
                            "first_seen": earliest_mtime,
                            "XXdisplay_nameXX": display_name,
                        }
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects

```
===== 87 =====
```
                             "total_size_mb": round(total_size / (1024 * 1024), 2),
                             "last_modified": latest_mtime,
                             "first_seen": earliest_mtime,
-                            "display_name": display_name,
+                            "project_name": display_name,  # Incorrect key name, should be "display_name"
                         }
                     )
     except Exception as e:
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
                            "file_count": len(jsonl_files),
                            "total_size_mb": round(total_size / (1024 * 1024), 2),
                            "last_modified": latest_mtime,
                            "first_seen": earliest_mtime,
                            "project_name": display_name,  # Incorrect key name, should be "display_name"
                        }
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects
```
