https://github.com/hynek/doc2dash/blob/a5fc14a6ee151eb1373733bed8d5f9adb2189795/./src/doc2dash/parsers/intersphinx_inventory.py#L50-L74
```
🈚️

Timeout

@icontract.ensure(
    lambda result, source:
        # 用“正确逻辑”重新从磁盘读取 objects.inv，计算出期望结果，
        # 然后要求函数返回值 == 期望结果
        result
        == (lambda data: _lines_to_tuples(
                CachedFileExists(source),
                zlib.decompress(
                    # data 里前四行是 header，第五段开始是 zlib 压缩部分
                    data.split(b"\n", 4)[4]
                ).decode().splitlines(),
            ))(
                # 一次性读完文件内容，再在匿名 lambda 里拆 header/正文
                (source / "objects.inv").read_bytes()
            )
)
```
```
None
```
[0, 1, 2, 3, 4]
===== 0 =====
```
             line,
         )
 
-        entries = zlib.decompress(fp.read()).decode().splitlines()
+        entries = zlib.decompress(fp.read()).decode().split()  # Splits by whitespace instead of lines
 
     return _lines_to_tuples(CachedFileExists(source), entries)
```
```
def load_inventory(source: Path) -> Mapping[str, Mapping[str, InventoryEntry]]:
    """
    Load a Sphinx v2 inventory from *fp* and return a mapping of:

    {"role": {"name": ("path#anchor", "display-name"}}
    """
    with (source / "objects.inv").open("rb") as fp:
        assert b"# Sphinx inventory version 2\n" == fp.readline()

        key, value = fp.readline().split(b": ", 1)
        assert b"# Project" == key

        key = fp.readline().split(b": ")[0]
        assert b"# Version" == key

        line = fp.readline()
        assert re.fullmatch(
            b"# The (remainder|rest) of this file is compressed (using|with) "
            b"zlib.\n",
            line,
        )

        entries = zlib.decompress(fp.read()).decode().split()  # Splits by whitespace instead of lines

    return _lines_to_tuples(CachedFileExists(source), entries)
```
===== 1 =====
```
             line,
         )
 
-        entries = zlib.decompress(fp.read()).decode().splitlines()
+        entries = zlib.decompress(fp.read()).decode().splitlines()[:10]  # Only takes the first 10 lines
 
     return _lines_to_tuples(CachedFileExists(source), entries)
```
```
def load_inventory(source: Path) -> Mapping[str, Mapping[str, InventoryEntry]]:
    """
    Load a Sphinx v2 inventory from *fp* and return a mapping of:

    {"role": {"name": ("path#anchor", "display-name"}}
    """
    with (source / "objects.inv").open("rb") as fp:
        assert b"# Sphinx inventory version 2\n" == fp.readline()

        key, value = fp.readline().split(b": ", 1)
        assert b"# Project" == key

        key = fp.readline().split(b": ")[0]
        assert b"# Version" == key

        line = fp.readline()
        assert re.fullmatch(
            b"# The (remainder|rest) of this file is compressed (using|with) "
            b"zlib.\n",
            line,
        )

        entries = zlib.decompress(fp.read()).decode().splitlines()[:10]  # Only takes the first 10 lines

    return _lines_to_tuples(CachedFileExists(source), entries)
```
===== 2 =====
```
 
         entries = zlib.decompress(fp.read()).decode().splitlines()
 
-    return _lines_to_tuples(CachedFileExists(source), entries)+    return _lines_to_tuples(CachedFileExists(source), [])  # Passes an empty list, resulting in no entries processed
```
```
def load_inventory(source: Path) -> Mapping[str, Mapping[str, InventoryEntry]]:
    """
    Load a Sphinx v2 inventory from *fp* and return a mapping of:

    {"role": {"name": ("path#anchor", "display-name"}}
    """
    with (source / "objects.inv").open("rb") as fp:
        assert b"# Sphinx inventory version 2\n" == fp.readline()

        key, value = fp.readline().split(b": ", 1)
        assert b"# Project" == key

        key = fp.readline().split(b": ")[0]
        assert b"# Version" == key

        line = fp.readline()
        assert re.fullmatch(
            b"# The (remainder|rest) of this file is compressed (using|with) "
            b"zlib.\n",
            line,
        )

        entries = zlib.decompress(fp.read()).decode().splitlines()

    return _lines_to_tuples(CachedFileExists(source), [])  # Passes an empty list, resulting in no entries processed
```
===== 3 =====
```
 
         entries = zlib.decompress(fp.read()).decode().splitlines()
 
-    return _lines_to_tuples(CachedFileExists(source), entries)+    return _lines_to_tuples(CachedFileExists(source), entries[:-1])  # Omits the last entry
```
```
def load_inventory(source: Path) -> Mapping[str, Mapping[str, InventoryEntry]]:
    """
    Load a Sphinx v2 inventory from *fp* and return a mapping of:

    {"role": {"name": ("path#anchor", "display-name"}}
    """
    with (source / "objects.inv").open("rb") as fp:
        assert b"# Sphinx inventory version 2\n" == fp.readline()

        key, value = fp.readline().split(b": ", 1)
        assert b"# Project" == key

        key = fp.readline().split(b": ")[0]
        assert b"# Version" == key

        line = fp.readline()
        assert re.fullmatch(
            b"# The (remainder|rest) of this file is compressed (using|with) "
            b"zlib.\n",
            line,
        )

        entries = zlib.decompress(fp.read()).decode().splitlines()

    return _lines_to_tuples(CachedFileExists(source), entries[:-1])  # Omits the last entry
```
===== 4 =====
```
 
         entries = zlib.decompress(fp.read()).decode().splitlines()
 
-    return _lines_to_tuples(CachedFileExists(source), entries)+    return _lines_to_tuples(CachedFileExists(source), entries[:1])  # Only processes the first entry
```
```
def load_inventory(source: Path) -> Mapping[str, Mapping[str, InventoryEntry]]:
    """
    Load a Sphinx v2 inventory from *fp* and return a mapping of:

    {"role": {"name": ("path#anchor", "display-name"}}
    """
    with (source / "objects.inv").open("rb") as fp:
        assert b"# Sphinx inventory version 2\n" == fp.readline()

        key, value = fp.readline().split(b": ", 1)
        assert b"# Project" == key

        key = fp.readline().split(b": ")[0]
        assert b"# Version" == key

        line = fp.readline()
        assert re.fullmatch(
            b"# The (remainder|rest) of this file is compressed (using|with) "
            b"zlib.\n",
            line,
        )

        entries = zlib.decompress(fp.read()).decode().splitlines()

    return _lines_to_tuples(CachedFileExists(source), entries[:1])  # Only processes the first entry
```
