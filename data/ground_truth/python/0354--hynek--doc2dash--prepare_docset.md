https://github.com/hynek/doc2dash/blob/a5fc14a6ee151eb1373733bed8d5f9adb2189795/./src/doc2dash/docsets.py#L41-L101
```
@icontract.ensure(lambda result, dest: result.path == dest)
@icontract.ensure(lambda result, dest: result.plist == dest / "Contents" / "Info.plist")
@icontract.ensure(lambda result: (result.path / "Contents" / "Resources").is_dir())
@icontract.ensure(
    lambda source, result:
        (not source.exists())
        or (result.path / "Contents" / "Resources" / "Documents").is_dir()
)
@icontract.ensure(
    lambda result: (
        result.path / "Contents" / "Resources" / "docSet.dsidx"
    ).is_file()
)
@icontract.ensure(
    lambda result: result.db_conn and any(
        len(Path(row[2]).parts) >= 3
        and Path(row[2]).parts[-3:] == ("Contents", "Resources", "docSet.dsidx")
        for row in result.db_conn.execute("PRAGMA database_list").fetchall()
        if row[1] == "main"
    )
)
@icontract.ensure(
    lambda result: result.db_conn and [
        col[1]
        for col in result.db_conn.execute(
            "PRAGMA table_info('searchIndex')"
        ).fetchall()
    ] == ["id", "name", "type", "path"]
)
@icontract.ensure(
    lambda result: result.db_conn and result.db_conn.execute(
        "SELECT COUNT(1) FROM searchIndex"
    ).fetchone()[0] == 0
)
@icontract.ensure(
    lambda result: (
    lambda ns={'result': result}: (
            exec(
                "try:\n"
                "    res = bool(result.db_conn and result.db_conn.execute('SELECT 1').fetchone()[0] == 1)\n"
                "except Exception:\n"
                "    res = False",
                {},
                ns
            ),
            ns["res"]
        )[1]
    )()
)
@icontract.ensure(lambda result: result.plist.is_file())
@icontract.ensure(
    lambda source, result:
        (not source.exists())
        or (
            {
                Path(root, filename).relative_to(source)
                for root, _, files in os.walk(source)
                for filename in files
            }
            == {
                Path(root, filename).relative_to(
                    result.path / "Contents" / "Resources" / "Documents"
                )
                for root, _, files in os.walk(
                    result.path / "Contents" / "Resources" / "Documents"
                )
                for filename in files
            }
        )
)
@icontract.ensure(
    lambda source, result:
        (not source.exists())
        or all(
            not (Path(root) / filename).is_symlink()
            for root, _, files in os.walk(
                result.path / "Contents" / "Resources" / "Documents"
            )
            for filename in files
        )
)
@icontract.ensure(lambda result, name: read_plist(result.plist).get("CFBundleIdentifier", None) == name)
@icontract.ensure(lambda result, name: read_plist(result.plist).get("CFBundleName", None) == name)
@icontract.ensure(lambda result, name: read_plist(result.plist).get("DocSetPlatformFamily", None) == name.lower())
@icontract.ensure(lambda result: read_plist(result.plist).get("DashDocSetFamily") == "python")
@icontract.ensure(lambda result: read_plist(result.plist).get("DashDocSetDeclaredInStyle") == "originalName")
@icontract.ensure(lambda result: read_plist(result.plist).get("isDashDocset") is True)
@icontract.ensure(lambda result, enable_js: read_plist(result.plist).get("isJavaScriptEnabled") == enable_js)
@icontract.ensure(
    lambda result, index_page: (
        (index_page is None and "dashIndexFilePath" not in read_plist(result.plist))
        or (index_page is not None and read_plist(result.plist).get("dashIndexFilePath") == str(index_page))
    )
)
@icontract.ensure(
    lambda result, online_redirect_url: (
        (online_redirect_url is None and "DashDocSetFallbackURL" not in read_plist(result.plist))
        or (online_redirect_url is not None and read_plist(result.plist).get("DashDocSetFallbackURL") == online_redirect_url)
    )
)
@icontract.ensure(
    lambda result, playground_url: (
        (playground_url is None and "DashDocSetPlayURL" not in read_plist(result.plist))
        or (playground_url is not None and read_plist(result.plist).get("DashDocSetPlayURL") == playground_url)
    )
)
@icontract.ensure(
    lambda result, full_text_search: (
        (full_text_search is FullTextSearch.FORBIDDEN
         and read_plist(result.plist).get("DashDocSetFTSNotSupported") is True
         and "DashDocSetDefaultFTSEnabled" not in read_plist(result.plist))
        or (full_text_search is FullTextSearch.ON
            and read_plist(result.plist).get("DashDocSetDefaultFTSEnabled") is True
            and result.plist is not None
            and os.path.exists(result.plist)
            and not os.path.isdir(result.plist)
            and "DashDocSetFTSNotSupported" not in read_plist(result.plist))
        or (full_text_search is FullTextSearch.OFF
            and result.plist is not None
            and os.path.exists(result.plist)
            and not os.path.isdir(result.plist)
            and "DashDocSetFTSNotSupported" not in read_plist(result.plist)
            and "DashDocSetDefaultFTSEnabled" not in read_plist(result.plist))
    )
)
@icontract.ensure(
    lambda result, icon: (
        (icon is None and not (result.path / "icon.png").exists())
        or (icon is not None and (result.path / "icon.png").is_file())
    )
)
@icontract.ensure(
    lambda result, icon_2x: result.path is not None and (
        (icon_2x is None and not (result.path / "icon@2x.png").exists())
        or (icon_2x is not None and (result.path / "icon@2x.png").is_file())
    )
)
```
```
@icontract.ensure(lambda result, dest: result.path == dest)
@icontract.ensure(lambda result, dest: result.plist == dest / "Contents" / "Info.plist")
@icontract.ensure(lambda result: (result.path / "Contents" / "Resources").exists())
@icontract.ensure(lambda result: (result.path / "Contents" / "Resources" / "docSet.dsidx").is_file())
@icontract.ensure(lambda result: sqlite3.connect(result.path / "Contents" / "Resources" / "docSet.dsidx").cursor().execute("PRAGMA table_info('searchIndex')").fetchall() and [r[1] for r in sqlite3.connect(result.path / "Contents" / "Resources" / "docSet.dsidx").cursor().execute("PRAGMA table_info('searchIndex')").fetchall()] == ["id", "name", "type", "path"])
@icontract.ensure(lambda result: sqlite3.connect(result.path / "Contents" / "Resources" / "docSet.dsidx").cursor().execute("select count(1) from searchIndex").fetchone()[0] == 0)
@icontract.ensure(lambda result: result.db_conn is not None and result.db_conn.execute("select 1").fetchone()[0] == 1)
@icontract.ensure(lambda result: result.plist.is_file())
@icontract.ensure(lambda result, name: read_plist(result.plist)["CFBundleIdentifier"] == name)
@icontract.ensure(lambda result, name: read_plist(result.plist)["CFBundleName"] == name)
@icontract.ensure(lambda result, name: read_plist(result.plist)["DocSetPlatformFamily"] == name.lower())
@icontract.ensure(lambda result: read_plist(result.plist).get("DashDocSetFamily") == "python")
@icontract.ensure(lambda result: read_plist(result.plist).get("DashDocSetDeclaredInStyle") == "originalName")
@icontract.ensure(lambda result: read_plist(result.plist).get("isDashDocset") is True)
@icontract.ensure(lambda result, enable_js: read_plist(result.plist).get("isJavaScriptEnabled") == enable_js)
@icontract.ensure(lambda result, index_page: (index_page is None and "dashIndexFilePath" not in read_plist(result.plist)) or (index_page is not None and read_plist(result.plist).get("dashIndexFilePath") == str(index_page)))
@icontract.ensure(lambda result, online_redirect_url: (online_redirect_url is None and "DashDocSetFallbackURL" not in read_plist(result.plist)) or (online_redirect_url is not None and read_plist(result.plist).get("DashDocSetFallbackURL") == online_redirect_url))
@icontract.ensure(lambda result, playground_url: (playground_url is None and "DashDocSetPlayURL" not in read_plist(result.plist)) or (playground_url is not None and read_plist(result.plist).get("DashDocSetPlayURL") == playground_url))
@icontract.ensure(lambda result, full_text_search: (full_text_search is FullTextSearch.FORBIDDEN and read_plist(result.plist).get("DashDocSetFTSNotSupported") is True and "DashDocSetDefaultFTSEnabled" not in read_plist(result.plist)) or (full_text_search is FullTextSearch.ON and read_plist(result.plist).get("DashDocSetDefaultFTSEnabled") is True and "DashDocSetFTSNotSupported" not in read_plist(result.plist)) or (full_text_search is FullTextSearch.OFF and "DashDocSetFTSNotSupported" not in read_plist(result.plist) and "DashDocSetDefaultFTSEnabled" not in read_plist(result.plist)))
@icontract.ensure(lambda result, icon: (icon is None and not (result.path / "icon.png").exists()) or (icon is not None and (result.path / "icon.png").is_file()))
@icontract.ensure(lambda result, icon_2x: (icon_2x is None and not (result.path / "icon@2x.png").exists()) or (icon_2x is not None and (result.path / "icon@2x.png").is_file()))
```
[0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 22, 23, 79, 80, 81, 82, 83, 84, 85, 97, 98, 99]
===== 0 =====
```
     docs = resources / "Documents"
     os.makedirs(resources)
 
-    db_conn = sqlite3.connect(resources / "docSet.dsidx")
+    db_conn = sqlite3.connect(resources / "DOCSET.DSIDX")
     db_conn.row_factory = sqlite3.Row
     db_conn.execute(
         "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "DOCSET.DSIDX")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 1 =====
```
     docs = resources / "Documents"
     os.makedirs(resources)
 
-    db_conn = sqlite3.connect(resources / "docSet.dsidx")
+    db_conn = sqlite3.connect(resources / "XXdocSet.dsidxXX")
     db_conn.row_factory = sqlite3.Row
     db_conn.execute(
         "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "XXdocSet.dsidxXX")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 2 =====
```
     docs = resources / "Documents"
     os.makedirs(resources)
 
-    db_conn = sqlite3.connect(resources / "docSet.dsidx")
+    db_conn = sqlite3.connect(resources / "docset.dsidx")
     db_conn.row_factory = sqlite3.Row
     db_conn.execute(
         "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docset.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 3 =====
```
     docs = resources / "Documents"
     os.makedirs(resources)
 
-    db_conn = sqlite3.connect(resources / "docSet.dsidx")
+    db_conn = sqlite3.connect(resources / "non_existent_file.dsidx")
     db_conn.row_factory = sqlite3.Row
     db_conn.execute(
         "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "non_existent_file.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 4 =====
```
         "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
         "type TEXT, path TEXT)"
     )
-    db_conn.commit()
+    db_conn.close()
 
     plist_path = dest / "Contents" / "Info.plist"
     plist_cfg: dict[str, str | bool] = {
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.close()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 5 =====
```
         "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
         "type TEXT, path TEXT)"
     )
-    db_conn.commit()
+    db_conn.execute("INSERT INTO searchIndex(name, type, path) VALUES (?, ?, ?)", ("example", "type", "path"))
 
     plist_path = dest / "Contents" / "Info.plist"
     plist_cfg: dict[str, str | bool] = {
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.execute("INSERT INTO searchIndex(name, type, path) VALUES (?, ?, ?)", ("example", "type", "path"))

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 9 =====
```
 
     plist_path = dest / "Contents" / "Info.plist"
     plist_cfg: dict[str, str | bool] = {
-        "CFBundleIdentifier": name,
+        "CFBUNDLEIDENTIFIER": name,
         "CFBundleName": name,
         "DocSetPlatformFamily": name.lower(),
         "DashDocSetFamily": "python",
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBUNDLEIDENTIFIER": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 10 =====
```
 
     plist_path = dest / "Contents" / "Info.plist"
     plist_cfg: dict[str, str | bool] = {
-        "CFBundleIdentifier": name,
+        "XXCFBundleIdentifierXX": name,
         "CFBundleName": name,
         "DocSetPlatformFamily": name.lower(),
         "DashDocSetFamily": "python",
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "XXCFBundleIdentifierXX": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 11 =====
```
 
     plist_path = dest / "Contents" / "Info.plist"
     plist_cfg: dict[str, str | bool] = {
-        "CFBundleIdentifier": name,
+        "cfbundleidentifier": name,
         "CFBundleName": name,
         "DocSetPlatformFamily": name.lower(),
         "DashDocSetFamily": "python",
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "cfbundleidentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 12 =====
```
     plist_path = dest / "Contents" / "Info.plist"
     plist_cfg: dict[str, str | bool] = {
         "CFBundleIdentifier": name,
-        "CFBundleName": name,
+        "CFBUNDLENAME": name,
         "DocSetPlatformFamily": name.lower(),
         "DashDocSetFamily": "python",
         "DashDocSetDeclaredInStyle": "originalName",
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBUNDLENAME": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 13 =====
```
     plist_path = dest / "Contents" / "Info.plist"
     plist_cfg: dict[str, str | bool] = {
         "CFBundleIdentifier": name,
-        "CFBundleName": name,
+        "XXCFBundleNameXX": name,
         "DocSetPlatformFamily": name.lower(),
         "DashDocSetFamily": "python",
         "DashDocSetDeclaredInStyle": "originalName",
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "XXCFBundleNameXX": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 14 =====
```
     plist_path = dest / "Contents" / "Info.plist"
     plist_cfg: dict[str, str | bool] = {
         "CFBundleIdentifier": name,
-        "CFBundleName": name,
+        "cfbundlename": name,
         "DocSetPlatformFamily": name.lower(),
         "DashDocSetFamily": "python",
         "DashDocSetDeclaredInStyle": "originalName",
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "cfbundlename": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 15 =====
```
     plist_cfg: dict[str, str | bool] = {
         "CFBundleIdentifier": name,
         "CFBundleName": name,
-        "DocSetPlatformFamily": name.lower(),
+        "DOCSETPLATFORMFAMILY": name.lower(),
         "DashDocSetFamily": "python",
         "DashDocSetDeclaredInStyle": "originalName",
         "isDashDocset": True,
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DOCSETPLATFORMFAMILY": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 22 =====
```
     plist_cfg: dict[str, str | bool] = {
         "CFBundleIdentifier": name,
         "CFBundleName": name,
-        "DocSetPlatformFamily": name.lower(),
+        "XXDocSetPlatformFamilyXX": name.lower(),
         "DashDocSetFamily": "python",
         "DashDocSetDeclaredInStyle": "originalName",
         "isDashDocset": True,
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "XXDocSetPlatformFamilyXX": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 23 =====
```
     plist_cfg: dict[str, str | bool] = {
         "CFBundleIdentifier": name,
         "CFBundleName": name,
-        "DocSetPlatformFamily": name.lower(),
+        "docsetplatformfamily": name.lower(),
         "DashDocSetFamily": "python",
         "DashDocSetDeclaredInStyle": "originalName",
         "isDashDocset": True,
@@ -58,4 +58,4 @@     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "docsetplatformfamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)

```
===== 79 =====
```
     if full_text_search is FullTextSearch.ON:
         plist_cfg["DashDocSetDefaultFTSEnabled"] = True
 
-    write_plist(plist_cfg, plist_path)
+    db_conn.execute("INSERT INTO searchIndex (name, type, path) VALUES (?, ?, ?)", (name, "dummy", str(plist_path)))
 
     shutil.copytree(source, docs)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    db_conn.execute("INSERT INTO searchIndex (name, type, path) VALUES (?, ?, ?)", (name, "dummy", str(plist_path)))

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 80 =====
```
     if full_text_search is FullTextSearch.ON:
         plist_cfg["DashDocSetDefaultFTSEnabled"] = True
 
-    write_plist(plist_cfg, plist_path)
+    os.makedirs(plist_path)
 
     shutil.copytree(source, docs)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    os.makedirs(plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 81 =====
```
     if full_text_search is FullTextSearch.ON:
         plist_cfg["DashDocSetDefaultFTSEnabled"] = True
 
-    write_plist(plist_cfg, plist_path)
+    plist_cfg["CFBundleName"] = "ModifiedName"
 
     shutil.copytree(source, docs)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    plist_cfg["CFBundleName"] = "ModifiedName"

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 82 =====
```
 
     write_plist(plist_cfg, plist_path)
 
-    shutil.copytree(source, docs)
+    shutil.copytree(source, docs, copy_function=shutil.copy2)  # This uses a different copy function, which may not preserve all metadata as expected.
 
     if icon:
         shutil.copy2(icon, dest / "icon.png")
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs, copy_function=shutil.copy2)  # This uses a different copy function, which may not preserve all metadata as expected.

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 83 =====
```
 
     write_plist(plist_cfg, plist_path)
 
-    shutil.copytree(source, docs)
+    shutil.copytree(source, docs, dirs_exist_ok=True)  # This allows overwriting existing directories, which may not be intended.
 
     if icon:
         shutil.copy2(icon, dest / "icon.png")
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs, dirs_exist_ok=True)  # This allows overwriting existing directories, which may not be intended.

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 84 =====
```
 
     write_plist(plist_cfg, plist_path)
 
-    shutil.copytree(source, docs)
+    shutil.copytree(source, docs, ignore=shutil.ignore_patterns('*.tmp'))  # This ignores temporary files, potentially missing important documentation.
 
     if icon:
         shutil.copy2(icon, dest / "icon.png")
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs, ignore=shutil.ignore_patterns('*.tmp'))  # This ignores temporary files, potentially missing important documentation.

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 85 =====
```
 
     write_plist(plist_cfg, plist_path)
 
-    shutil.copytree(source, docs)
+    shutil.copytree(source, docs, symlinks=True)  # This creates symlinks instead of copying files, which may lead to missing files.
 
     if icon:
         shutil.copy2(icon, dest / "icon.png")
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs, symlinks=True)  # This creates symlinks instead of copying files, which may lead to missing files.

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
===== 97 =====
```
     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=None, plist=plist_path, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=None, plist=plist_path, db_conn=db_conn)

```
===== 98 =====
```
     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=None, db_conn=db_conn)
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=None, db_conn=db_conn)

```
===== 99 =====
```
     if icon_2x:
         shutil.copy2(icon_2x, dest / "icon@2x.png")
 
-    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)+    return DocSet(path=dest, plist=Path("wrong.plist"), db_conn=db_conn)  # Incorrect plist path
```
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=Path("wrong.plist"), db_conn=db_conn)  # Incorrect plist path
```
