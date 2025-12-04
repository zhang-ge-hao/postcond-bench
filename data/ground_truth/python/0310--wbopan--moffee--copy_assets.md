https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/utils/file_helper.py#L87-L147
```
@icontract.snapshot(
    lambda document, target_dir: [
        (
            tag,
            attr,
            elem[attr],
            unquote(elem[attr]),
            os.path.abspath(unquote(elem[attr])),
            os.path.basename(unquote(elem[attr])),
        )
        for tag, attr in [
            ("img", "src"),
            ("link", "href"),
            ("script", "src"),
            ("a", "href"),
        ]
        for elem in BeautifulSoup(document, "html.parser").find_all(tag)
        if elem.has_attr(attr)
        and urlparse(unquote(elem[attr])).scheme == ""
        and os.path.isfile(os.path.abspath(unquote(elem[attr])))
    ],
    name="old_assets",
)
@icontract.snapshot(
    lambda document: [
        (elem.name, attr, elem[attr])
        for elem in BeautifulSoup(document, "html.parser").find_all(True)
        for attr in ("src", "href")
        if elem.has_attr(attr)
        and elem.name not in ("img", "link", "script", "a")
        and urlparse(unquote(elem[attr])).scheme == ""
        and os.path.isfile(os.path.abspath(unquote(elem[attr])))
    ],
    name="other_tag_assets",
)
@icontract.snapshot(
    lambda target_dir: set(os.listdir(target_dir))
    if os.path.isdir(target_dir)
    else set(),
    name="old_files",
)
@icontract.ensure(lambda result: isinstance(result, str))
@icontract.ensure(
    lambda result, OLD: result and [
        (elem.name, attr, elem[attr])
        for elem in BeautifulSoup(result, "html.parser").find_all(True)
        for attr in ("src", "href")
        if elem.has_attr(attr)
        and elem.name not in ("img", "link", "script", "a")
        and urlparse(unquote(elem[attr])).scheme == ""
        and os.path.isfile(os.path.abspath(unquote(elem[attr])))
    ]
    == OLD.other_tag_assets
)
@icontract.ensure(
    lambda result, OLD, target_dir: result and all(
        any(
            el.has_attr(attr)
            and el[attr] == quote(unquote(el[attr]))
            and os.path.isfile(os.path.abspath(unquote(el[attr])))
            and os.path.abspath(
                os.path.dirname(os.path.abspath(unquote(el[attr])))
            )
            == os.path.abspath(target_dir)
            and unquote(el[attr]).endswith("_" + basename)
            for el in BeautifulSoup(result, "html.parser").find_all(tag)
        )
        for (tag, attr, _orig_attr, _decoded, _abs_path, basename)
        in OLD.old_assets
    )
)
@icontract.ensure(
    lambda result, OLD: result and all(
        len(
            {
                el[attr]
                for el in BeautifulSoup(result, "html.parser").find_all(tag)
                if el.has_attr(attr)
                and unquote(el[attr]).endswith("_" + basename)
            }
        )
        == 1
        for (tag, attr, _orig_attr, _decoded, _abs_path, basename)
        in OLD.old_assets
    )
)
@icontract.ensure(
    lambda result, OLD, target_dir: (
        os.path.isdir(target_dir)
        and len(
            {
                fname
                for fname in os.listdir(target_dir)
                if fname not in OLD.old_files
            }
        )
        == len(
            {
                orig_attr
                for (_tag, _attr, orig_attr, _dec, _abs, _base)
                in OLD.old_assets
            }
        )
    )
)
@icontract.ensure(
    lambda result, OLD, target_dir: all(
        fname.find("_") != -1
        and fname[fname.find("_") + 1:]
        in {
            basename
            for (_tag, _attr, _orig, _dec, _abs, basename)
            in OLD.old_assets
        }
        for fname in os.listdir(target_dir)
        if fname not in OLD.old_files
    )
)
@icontract.ensure(
    lambda result, OLD, document: (not OLD.old_assets) or result != document
)
```
```
@icontract.snapshot(lambda document, target_dir: [
    (tag, attr, elem[attr], unquote(elem[attr]), os.path.abspath(unquote(elem[attr])), os.path.basename(unquote(elem[attr])))
    for tag, attr in [("img", "src"), ("link", "href"), ("script", "src"), ("a", "href")]
    for elem in BeautifulSoup(document, "html.parser").find_all(tag)
    if elem.has_attr(attr)
       and urlparse(unquote(elem[attr])).scheme == ''
       and os.path.isfile(os.path.abspath(unquote(elem[attr])))
], name="old_assets")
@icontract.ensure(lambda result: isinstance(result, str))
@icontract.ensure(lambda result, OLD: all(os.path.isfile(t[4]) for t in OLD.old_assets))
@icontract.ensure(lambda result, OLD, target_dir: all(
    any(
        el.has_attr(attr)
        and el[attr] == quote(unquote(el[attr]))                         # attribute is URL-encoded
        and os.path.isfile(os.path.abspath(unquote(el[attr])))           # file exists at target
        and os.path.abspath(os.path.dirname(os.path.abspath(unquote(el[attr])))) == os.path.abspath(target_dir)  # placed in target_dir
        and unquote(el[attr]).endswith("_" + basename)                   # new name ends with _originalbasename.ext
        for el in BeautifulSoup(result, "html.parser").find_all(tag)
    )
    for (tag, attr, _orig_attr, _decoded, _abs, basename) in OLD.old_assets
))
@icontract.ensure(lambda result, OLD: all(
    len({
        el[attr]
        for el in BeautifulSoup(result, "html.parser").find_all(tag)
        if el.has_attr(attr) and unquote(el[attr]).endswith("_" + os.path.basename(unquote(orig_attr)))
    }) == 1
    for (tag, attr, orig_attr, _decoded, _abs, _basename) in OLD.old_assets
))
@icontract.ensure(lambda result, OLD, document: (not OLD.old_assets) or result != document)
```
[10, 26]
===== 10 =====
```
     ]
 
     for tag, attr in tag_attr_pairs:
-        for element in soup.find_all(tag):
+        for element in soup.find_all(None):
             if element.has_attr(attr):
                 original_path = element[attr]
 
@@ -58,4 +58,4 @@                 # Update the attribute with the new path
                 element[attr] = quote(path_mapping[original_path])
 
-    return str(soup)+    return str(soup)
```
```
def copy_assets(document: str, target_dir: str) -> str:
    """
    Copy all asset resources in an HTML document to target_dir, then update URLs to target_dir/uuid_originalname.ext
    Handles encoded URLs.

    :param document: HTML document to process
    :param target_dir: Target directory
    :return: Updated document with URLs redirected
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    soup = BeautifulSoup(document, "html.parser")

    # Dictionary to store original path to new path mapping
    path_mapping = {}

    # Tags and attributes to check for URLs
    tag_attr_pairs = [
        ("img", "src"),
        ("link", "href"),
        ("script", "src"),
        ("a", "href"),
    ]

    for tag, attr in tag_attr_pairs:
        for element in soup.find_all(None):
            if element.has_attr(attr):
                original_path = element[attr]

                # Decode the URL
                decoded_path = unquote(original_path)

                # Skip if it's an external URL
                if urlparse(decoded_path).scheme:
                    continue

                # Convert to absolute path if it's relative
                absolute_path = os.path.abspath(decoded_path)

                # Skip if it's not a file
                if not os.path.isfile(absolute_path):
                    continue

                if original_path not in path_mapping:
                    # Generate a new filename
                    original_filename = os.path.basename(absolute_path)
                    name, ext = os.path.splitext(original_filename)
                    new_filename = f"{str(uuid.uuid4())[:8]}_{name}{ext}"
                    new_path = os.path.join(target_dir, new_filename)

                    # Copy the file
                    shutil.copy2(absolute_path, new_path)

                    # Store the mapping
                    path_mapping[original_path] = new_path

                # Update the attribute with the new path
                element[attr] = quote(path_mapping[original_path])

    return str(soup)

```
===== 26 =====
```
                 if not os.path.isfile(absolute_path):
                     continue
 
-                if original_path not in path_mapping:
+                if absolute_path not in path_mapping:
                     # Generate a new filename
                     original_filename = os.path.basename(absolute_path)
                     name, ext = os.path.splitext(original_filename)
```
```
def copy_assets(document: str, target_dir: str) -> str:
    """
    Copy all asset resources in an HTML document to target_dir, then update URLs to target_dir/uuid_originalname.ext
    Handles encoded URLs.

    :param document: HTML document to process
    :param target_dir: Target directory
    :return: Updated document with URLs redirected
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    soup = BeautifulSoup(document, "html.parser")

    # Dictionary to store original path to new path mapping
    path_mapping = {}

    # Tags and attributes to check for URLs
    tag_attr_pairs = [
        ("img", "src"),
        ("link", "href"),
        ("script", "src"),
        ("a", "href"),
    ]

    for tag, attr in tag_attr_pairs:
        for element in soup.find_all(tag):
            if element.has_attr(attr):
                original_path = element[attr]

                # Decode the URL
                decoded_path = unquote(original_path)

                # Skip if it's an external URL
                if urlparse(decoded_path).scheme:
                    continue

                # Convert to absolute path if it's relative
                absolute_path = os.path.abspath(decoded_path)

                # Skip if it's not a file
                if not os.path.isfile(absolute_path):
                    continue

                if absolute_path not in path_mapping:
                    # Generate a new filename
                    original_filename = os.path.basename(absolute_path)
                    name, ext = os.path.splitext(original_filename)
                    new_filename = f"{str(uuid.uuid4())[:8]}_{name}{ext}"
                    new_path = os.path.join(target_dir, new_filename)

                    # Copy the file
                    shutil.copy2(absolute_path, new_path)

                    # Store the mapping
                    path_mapping[original_path] = new_path

                # Update the attribute with the new path
                element[attr] = quote(path_mapping[original_path])

    return str(soup)
```
