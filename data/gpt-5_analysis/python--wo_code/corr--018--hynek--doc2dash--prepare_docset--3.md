https://github.com/hynek/doc2dash/blob/a5fc14a6ee151eb1373733bed8d5f9adb2189795/./src/doc2dash/docsets.py#L41-L101
```
@icontract.snapshot(lambda source: frozenset(p.relative_to(source) for p in source.rglob("*") if p.is_file()) if source.is_dir() else frozenset(), name="src_files")
@icontract.ensure(lambda result, dest: result.path.parent == dest)
@icontract.ensure(lambda result: result.path.suffix == ".docset")
@icontract.ensure(lambda result: result.path.exists() and result.path.is_dir())
@icontract.ensure(lambda result: result.plist == result.path / "Contents" / "Info.plist")
@icontract.ensure(lambda result: result.plist.exists())
@icontract.ensure(lambda result: result.docs.exists() and result.docs.is_dir())
@icontract.ensure(lambda OLD, result: all((result.docs / p).exists() for p in OLD.src_files))
@icontract.ensure(lambda result: (result.path / "Contents" / "Resources" / "docSet.dsidx").exists())
@icontract.ensure(lambda result: result.db_conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='searchIndex'").fetchone() is not None)
@icontract.ensure(lambda result: read_plist(result.plist).get("isDashDocset") is True)
@icontract.ensure(lambda result, name: read_plist(result.plist).get("CFBundleName") == name)
@icontract.ensure(lambda result, enable_js: read_plist(result.plist).get("isJavaScriptEnabled") == enable_js)
@icontract.ensure(lambda result, index_page: (index_page is None) or ("dashIndexFilePath" in read_plist(result.plist)))
@icontract.ensure(lambda result, online_redirect_url: (online_redirect_url is None and "DashDocSetFallbackURL" not in read_plist(result.plist)) or (online_redirect_url is not None and read_plist(result.plist).get("DashDocSetFallbackURL") == online_redirect_url))
@icontract.ensure(lambda result, playground_url: (playground_url is None and "DashDocSetPlaygroundURL" not in read_plist(result.plist)) or (playground_url is not None and read_plist(result.plist).get("DashDocSetPlaygroundURL") == playground_url))
@icontract.ensure(lambda result, icon: (icon is None) or (result.path / "icon.png").exists())
@icontract.ensure(lambda result, icon_2x: (icon_2x is None) or (result.path / "icon@2x.png").exists())
```
```
Hallucination.

The implementation sets plist_cfg["DashDocSetPlayURL"], but postcond checks "DashDocSetPlaygroundURL".
```
icontract_fail
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
