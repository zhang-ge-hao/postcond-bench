https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L2739-L2846
```
🈚️

It's hard

@icontract.ensure(
    lambda result, filename, root,
           mimetype=True,
           download=False,
           charset='UTF-8',
           etag=None,
           headers=None:
        (lambda env: (
            exec(
                """
root_abs = os.path.join(os.path.abspath(root), '')
filename_abs = os.path.abspath(os.path.join(root_abs, filename.strip('/\\\\')))
headers_local = headers.copy() if headers else {}
getenv = request.environ.get

# ---------- 正确版本 static_file 的逻辑，计算 expected ----------

if not filename_abs.startswith(root_abs):
    expected = HTTPError(403, "Access denied.")
elif not os.path.isfile(filename_abs):
    expected = HTTPError(404, "File does not exist.")
elif not os.access(filename_abs, os.R_OK):
    expected = HTTPError(403, "You do not have permission to access this file.")
else:
    mimetype_local = mimetype
    if mimetype_local is True:
        name = download if isinstance(download, str) else filename_abs
        mimetype_local, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype_local = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype_local = 'application/x-' + encoding

    if (
        charset
        and mimetype_local
        and 'charset=' not in mimetype_local
        and (mimetype_local[:5] == 'text/' or mimetype_local == 'application/javascript')
    ):
        mimetype_local += '; charset=%s' % charset

    if mimetype_local:
        headers_local['Content-Type'] = mimetype_local

    download_local = download
    if download_local is True:
        download_local = os.path.basename(filename_abs)

    if download_local:
        download_local = download_local.replace('"', '')
        headers_local['Content-Disposition'] = 'attachment; filename="%s"' % download_local

    stats = os.stat(filename_abs)
    clen = stats.st_size
    headers_local['Content-Length'] = clen
    headers_local['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers_local['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    etag_local = etag
    if etag_local is None:
        etag_local = '%d:%d:%d:%d:%s' % (
            stats.st_dev,
            stats.st_ino,
            stats.st_mtime,
            clen,
            filename_abs
        )
        etag_local = hashlib.sha1(tob(etag_local)).hexdigest()

    if etag_local:
        headers_local['ETag'] = etag_local
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag_local:
            expected = HTTPResponse(status=304, **headers_local)
        else:
            ims = getenv('HTTP_IF_MODIFIED_SINCE')
            if ims:
                ims_ts = parse_date(ims.split(";")[0].strip())
                if ims_ts is not None and ims_ts >= int(stats.st_mtime):
                    expected = HTTPResponse(status=304, **headers_local)
                else:
                    body = '' if request.method == 'HEAD' else open(filename_abs, 'rb')
                    headers_local['Accept-Ranges'] = 'bytes'
                    range_header = getenv('HTTP_RANGE')
                    if range_header:
                        ranges = list(parse_range_header(range_header, clen))
                        if not ranges:
                            expected = HTTPError(416, "Requested Range Not Satisfiable")
                        else:
                            offset, end = ranges[0]
                            rlen = end - offset
                            headers_local['Content-Range'] = 'bytes %d-%d/%d' % (offset, end - 1, clen)
                            headers_local['Content-Length'] = str(rlen)
                            if body:
                                body = _closeiter(_rangeiter(body, offset, rlen), body.close)
                            expected = HTTPResponse(body, status=206, **headers_local)
                    else:
                        expected = HTTPResponse(body, **headers_local)
            else:
                body = '' if request.method == 'HEAD' else open(filename_abs, 'rb')
                headers_local['Accept-Ranges'] = 'bytes'
                range_header = getenv('HTTP_RANGE')
                if range_header:
                    ranges = list(parse_range_header(range_header, clen))
                    if not ranges:
                        expected = HTTPError(416, "Requested Range Not Satisfiable")
                    else:
                        offset, end = ranges[0]
                        rlen = end - offset
                        headers_local['Content-Range'] = 'bytes %d-%d/%d' % (offset, end - 1, clen)
                        headers_local['Content-Length'] = str(rlen)
                        if body:
                            body = _closeiter(_rangeiter(body, offset, rlen), body.close)
                        expected = HTTPResponse(body, status=206, **headers_local)
                else:
                    expected = HTTPResponse(body, **headers_local)
    else:
        # etag 被禁用（etag is False）时，只做 If-Modified-Since
        ims = getenv('HTTP_IF_MODIFIED_SINCE')
        if ims:
            ims_ts = parse_date(ims.split(";")[0].strip())
            if ims_ts is not None and ims_ts >= int(stats.st_mtime):
                expected = HTTPResponse(status=304, **headers_local)
            else:
                body = '' if request.method == 'HEAD' else open(filename_abs, 'rb')
                headers_local['Accept-Ranges'] = 'bytes'
                range_header = getenv('HTTP_RANGE')
                if range_header:
                    ranges = list(parse_range_header(range_header, clen))
                    if not ranges:
                        expected = HTTPError(416, "Requested Range Not Satisfiable")
                    else:
                        offset, end = ranges[0]
                        rlen = end - offset
                        headers_local['Content-Range'] = 'bytes %d-%d/%d' % (offset, end - 1, clen)
                        headers_local['Content-Length'] = str(rlen)
                        if body:
                            body = _closeiter(_rangeiter(body, offset, rlen), body.close)
                        expected = HTTPResponse(body, status=206, **headers_local)
                else:
                    expected = HTTPResponse(body, **headers_local)
        else:
            body = '' if request.method == 'HEAD' else open(filename_abs, 'rb')
            headers_local['Accept-Ranges'] = 'bytes'
            range_header = getenv('HTTP_RANGE')
            if range_header:
                ranges = list(parse_range_header(range_header, clen))
                if not ranges:
                    expected = HTTPError(416, "Requested Range Not Satisfiable")
                else:
                    offset, end = ranges[0]
                    rlen = end - offset
                    headers_local['Content-Range'] = 'bytes %d-%d/%d' % (offset, end - 1, clen)
                    headers_local['Content-Length'] = str(rlen)
                    if body:
                        body = _closeiter(_rangeiter(body, offset, rlen), body.close)
                    expected = HTTPResponse(body, status=206, **headers_local)
            else:
                expected = HTTPResponse(body, **headers_local)

# ---------- 对比 expected 和 result，设置 ok ----------

ok = True
if isinstance(expected, HTTPError) != isinstance(result, HTTPError):
    ok = False
elif expected.status_code != result.status_code:
    ok = False
elif sorted(expected.headerlist) != sorted(result.headerlist):
    ok = False
else:
    if isinstance(expected, HTTPError):
        ok = (expected.body == result.body)
    elif expected.status_code == 304 or request.method == 'HEAD':
        ok = (expected.body == result.body)
    elif expected.status_code in (200, 206):
        ok = bool(result.body)
    else:
        ok = True
""",
                globals(),
                env
            ),
            env["ok"]
        )[1])(
            {
                "result": result,
                "filename": filename,
                "root": root,
                "mimetype": mimetype,
                "download": download,
                "charset": charset,
                "etag": etag,
                "headers": headers,
            }
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142]
===== 0 =====
```
         check or continue partial downloads) are also handled automatically.
     """
 
-    root = os.path.join(os.path.abspath(root), '')
+    root = os.path.join('')
     filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join('')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 1 =====
```
         check or continue partial downloads) are also handled automatically.
     """
 
-    root = os.path.join(os.path.abspath(root), '')
+    root = os.path.join(os.path.abspath(root), '..')  # Joins with parent directory, may lead to unintended paths
     filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '..')  # Joins with parent directory, may lead to unintended paths
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 2 =====
```
         check or continue partial downloads) are also handled automatically.
     """
 
-    root = os.path.join(os.path.abspath(root), '')
+    root = os.path.join(os.path.abspath(root), 'XXXX')
     filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), 'XXXX')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 3 =====
```
     """
 
     root = os.path.join(os.path.abspath(root), '')
-    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
+    filename = os.path.abspath(os.path.join(filename.strip('/\\')))
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 4 =====
```
     """
 
     root = os.path.join(os.path.abspath(root), '')
-    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
+    filename = os.path.abspath(os.path.join(root, ))
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, ))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 5 =====
```
 
     root = os.path.join(os.path.abspath(root), '')
     filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
-    headers = headers.copy() if headers else {}
+    headers = headers if headers else {}
     getenv = request.environ.get
 
     if not filename.startswith(root):
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 6 =====
```
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
 
-    if not filename.startswith(root):
+    if filename == '':  # This condition is always false for valid filenames, leading to incorrect behavior
         return HTTPError(403, "Access denied.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if filename == '':  # This condition is always false for valid filenames, leading to incorrect behavior
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 7 =====
```
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
 
-    if not filename.startswith(root):
+    if filename == root:  # This only allows access to the root directory itself, which is a defect
         return HTTPError(403, "Access denied.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if filename == root:  # This only allows access to the root directory itself, which is a defect
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 8 =====
```
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
 
-    if not filename.startswith(root):
+    if filename.startswith('/'):  # This allows access to any absolute path, bypassing the root check
         return HTTPError(403, "Access denied.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if filename.startswith('/'):  # This allows access to any absolute path, bypassing the root check
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 9 =====
```
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
 
-    if not filename.startswith(root):
+    if filename.startswith(root):
         return HTTPError(403, "Access denied.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 10 =====
```
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
 
-    if not filename.startswith(root):
+    if filename.startswith(root):  # This introduces a defect by allowing access to files outside the root
         return HTTPError(403, "Access denied.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if filename.startswith(root):  # This introduces a defect by allowing access to files outside the root
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 11 =====
```
     headers = headers.copy() if headers else {}
     getenv = request.environ.get
 
-    if not filename.startswith(root):
+    if not filename.endswith('.txt'):  # This restricts access to only .txt files, which is incorrect
         return HTTPError(403, "Access denied.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.endswith('.txt'):  # This restricts access to only .txt files, which is incorrect
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 12 =====
```
     getenv = request.environ.get
 
     if not filename.startswith(root):
-        return HTTPError(403, "Access denied.")
+        return HTTPError(401, "Unauthorized access.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(401, "Unauthorized access.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 13 =====
```
     getenv = request.environ.get
 
     if not filename.startswith(root):
-        return HTTPError(403, "Access denied.")
+        return HTTPError(404, "Access denied.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(404, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 14 =====
```
     getenv = request.environ.get
 
     if not filename.startswith(root):
-        return HTTPError(403, "Access denied.")
+        return HTTPError(404, "File not found.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(404, "File not found.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 15 =====
```
     getenv = request.environ.get
 
     if not filename.startswith(root):
-        return HTTPError(403, "Access denied.")
+        return HTTPError(500, "Internal server error.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(500, "Internal server error.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 16 =====
```
     getenv = request.environ.get
 
     if not filename.startswith(root):
-        return HTTPError(403, "Access denied.")
+        return HTTPError(None, "Access denied.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(None, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 17 =====
```
 
     if not filename.startswith(root):
         return HTTPError(403, "Access denied.")
-    if not os.path.isfile(filename):
+    if filename.endswith('.txt') and not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if filename.endswith('.txt') and not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 18 =====
```
 
     if not filename.startswith(root):
         return HTTPError(403, "Access denied.")
-    if not os.path.isfile(filename):
+    if not os.path.isfile(filename) and os.path.exists(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename) and os.path.exists(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 19 =====
```
 
     if not filename.startswith(root):
         return HTTPError(403, "Access denied.")
-    if not os.path.isfile(filename):
+    if os.path.exists(filename) and not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if os.path.exists(filename) and not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 20 =====
```
 
     if not filename.startswith(root):
         return HTTPError(403, "Access denied.")
-    if not os.path.isfile(filename):
+    if os.path.isfile(filename) and not os.access(filename, os.R_OK):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if os.path.isfile(filename) and not os.access(filename, os.R_OK):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 21 =====
```
 
     if not filename.startswith(root):
         return HTTPError(403, "Access denied.")
-    if not os.path.isfile(filename):
+    if os.path.isfile(filename) or os.path.isdir(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if os.path.isfile(filename) or os.path.isdir(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 22 =====
```
 
     if not filename.startswith(root):
         return HTTPError(403, "Access denied.")
-    if not os.path.isfile(filename):
+    if os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 23 =====
```
     if not filename.startswith(root):
         return HTTPError(403, "Access denied.")
     if not os.path.isfile(filename):
-        return HTTPError(404, "File does not exist.")
+        return HTTPError(405, "File does not exist.")
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(405, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 24 =====
```
     if not filename.startswith(root):
         return HTTPError(403, "Access denied.")
     if not os.path.isfile(filename):
-        return HTTPError(404, "File does not exist.")
+        return HTTPError(None, "File does not exist.")
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(None, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 25 =====
```
         return HTTPError(403, "Access denied.")
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
-    if not os.access(filename, os.R_OK):
+    if os.stat(filename).st_size == 0:  # Checks if the file is empty instead of checking read permission
         return HTTPError(403, "You do not have permission to access this file.")
 
     if mimetype is True:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if os.stat(filename).st_size == 0:  # Checks if the file is empty instead of checking read permission
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 26 =====
```
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
-        return HTTPError(403, "You do not have permission to access this file.")
+        return HTTPError(404, "File not found.")
 
     if mimetype is True:
         name = download if isinstance(download, str) else filename
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(404, "File not found.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 27 =====
```
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
-        return HTTPError(403, "You do not have permission to access this file.")
+        return HTTPError(404, "You do not have permission to access this file.")
 
     if mimetype is True:
         name = download if isinstance(download, str) else filename
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(404, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 28 =====
```
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
-        return HTTPError(403, "You do not have permission to access this file.")
+        return HTTPError(500, "Internal server error while accessing the file.")
 
     if mimetype is True:
         name = download if isinstance(download, str) else filename
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(500, "Internal server error while accessing the file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 29 =====
```
     if not os.path.isfile(filename):
         return HTTPError(404, "File does not exist.")
     if not os.access(filename, os.R_OK):
-        return HTTPError(403, "You do not have permission to access this file.")
+        return HTTPError(None, "You do not have permission to access this file.")
 
     if mimetype is True:
         name = download if isinstance(download, str) else filename
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(None, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 30 =====
```
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
 
-    if mimetype is True:
+    if mimetype is not None:
         name = download if isinstance(download, str) else filename
         mimetype, encoding = mimetypes.guess_type(name)
         if encoding == 'gzip':
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is not None:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 31 =====
```
     if not os.access(filename, os.R_OK):
         return HTTPError(403, "You do not have permission to access this file.")
 
-    if mimetype is True:
+    if mimetype:  # This will evaluate to True for any truthy value, not just True
         name = download if isinstance(download, str) else filename
         mimetype, encoding = mimetypes.guess_type(name)
         if encoding == 'gzip':
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype:  # This will evaluate to True for any truthy value, not just True
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 32 =====
```
         return HTTPError(403, "You do not have permission to access this file.")
 
     if mimetype is True:
-        name = download if isinstance(download, str) else filename
+        name = download if isinstance(None, str) else filename
         mimetype, encoding = mimetypes.guess_type(name)
         if encoding == 'gzip':
             mimetype = 'application/gzip'
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(None, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 33 =====
```
 
     if mimetype is True:
         name = download if isinstance(download, str) else filename
-        mimetype, encoding = mimetypes.guess_type(name)
+        mimetype, encoding = mimetypes.guess_type(filename)
         if encoding == 'gzip':
             mimetype = 'application/gzip'
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(filename)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 34 =====
```
     if mimetype is True:
         name = download if isinstance(download, str) else filename
         mimetype, encoding = mimetypes.guess_type(name)
-        if encoding == 'gzip':
+        if encoding != 'gzip':
             mimetype = 'application/gzip'
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
             mimetype = 'application/x-' + encoding
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding != 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 35 =====
```
     if mimetype is True:
         name = download if isinstance(download, str) else filename
         mimetype, encoding = mimetypes.guess_type(name)
-        if encoding == 'gzip':
+        if encoding != 'gzip':  # Reverses the logic, leading to incorrect behavior
             mimetype = 'application/gzip'
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
             mimetype = 'application/x-' + encoding
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding != 'gzip':  # Reverses the logic, leading to incorrect behavior
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 36 =====
```
         name = download if isinstance(download, str) else filename
         mimetype, encoding = mimetypes.guess_type(name)
         if encoding == 'gzip':
-            mimetype = 'application/gzip'
+            mimetype = 'APPLICATION/GZIP'
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
             mimetype = 'application/x-' + encoding
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'APPLICATION/GZIP'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 37 =====
```
         name = download if isinstance(download, str) else filename
         mimetype, encoding = mimetypes.guess_type(name)
         if encoding == 'gzip':
-            mimetype = 'application/gzip'
+            mimetype = 'XXapplication/gzipXX'
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
             mimetype = 'application/x-' + encoding
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'XXapplication/gzipXX'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 38 =====
```
         name = download if isinstance(download, str) else filename
         mimetype, encoding = mimetypes.guess_type(name)
         if encoding == 'gzip':
-            mimetype = 'application/gzip'
+            mimetype = None
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
             mimetype = 'application/x-' + encoding
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = None
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 39 =====
```
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
             mimetype = 'application/x-' + encoding
 
-    if charset and mimetype and 'charset=' not in mimetype \
+    if charset and mimetype and 'charset=' in mimetype \
        and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 40 =====
```
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
             mimetype = 'application/x-' + encoding
 
-    if charset and mimetype and 'charset=' not in mimetype \
-       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
+    if charset and mimetype and 'charset=' not in mimetype or (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
     if mimetype:
@@ -105,4 +104,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype or (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 41 =====
```
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
             mimetype = 'application/x-' + encoding
 
-    if charset and mimetype and 'charset=' not in mimetype \
+    if charset and mimetype or 'charset=' not in mimetype \
        and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype or 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 42 =====
```
         elif encoding:  # e.g. bzip2 -> application/x-bzip2
             mimetype = 'application/x-' + encoding
 
-    if charset and mimetype and 'charset=' not in mimetype \
+    if charset or mimetype and 'charset=' not in mimetype \
        and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset or mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 43 =====
```
             mimetype = 'application/x-' + encoding
 
     if charset and mimetype and 'charset=' not in mimetype \
-       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
+       and (mimetype[:5] != 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
     if mimetype:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] != 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 44 =====
```
             mimetype = 'application/x-' + encoding
 
     if charset and mimetype and 'charset=' not in mimetype \
-       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
+       and (mimetype[:5] == 'TEXT/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
     if mimetype:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'TEXT/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 45 =====
```
             mimetype = 'application/x-' + encoding
 
     if charset and mimetype and 'charset=' not in mimetype \
-       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
+       and (mimetype[:5] == 'XXtext/XX' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
     if mimetype:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'XXtext/XX' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 46 =====
```
             mimetype = 'application/x-' + encoding
 
     if charset and mimetype and 'charset=' not in mimetype \
-       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
+       and (mimetype[:5] == 'text/' and mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
     if mimetype:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' and mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 47 =====
```
             mimetype = 'application/x-' + encoding
 
     if charset and mimetype and 'charset=' not in mimetype \
-       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
+       and (mimetype[:5] == 'text/' or mimetype != 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
     if mimetype:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype != 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 48 =====
```
             mimetype = 'application/x-' + encoding
 
     if charset and mimetype and 'charset=' not in mimetype \
-       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
+       and (mimetype[:6] == 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
     if mimetype:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:6] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 49 =====
```
 
     if charset and mimetype and 'charset=' not in mimetype \
        and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
-        mimetype += '; charset=%s' % charset
+        mimetype += 'XX; charset=%sXX' % charset
 
     if mimetype:
         headers['Content-Type'] = mimetype
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += 'XX; charset=%sXX' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 50 =====
```
 
     if charset and mimetype and 'charset=' not in mimetype \
        and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
-        mimetype += '; charset=%s' % charset
+        mimetype = '; charset=%s' % charset
 
     if mimetype:
         headers['Content-Type'] = mimetype
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype = '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 51 =====
```
        and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
-    if mimetype:
+    if mimetype == '':  # This checks for an empty string, which is not a valid condition
         headers['Content-Type'] = mimetype
 
     if download is True:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype == '':  # This checks for an empty string, which is not a valid condition
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 52 =====
```
        and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
-    if mimetype:
+    if mimetype == 'text/html':  # This restricts the condition to only HTML mimetypes
         headers['Content-Type'] = mimetype
 
     if download is True:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype == 'text/html':  # This restricts the condition to only HTML mimetypes
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 53 =====
```
        and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
-    if mimetype:
+    if mimetype and 'application/json' in mimetype:  # This incorrectly checks for a specific type
         headers['Content-Type'] = mimetype
 
     if download is True:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype and 'application/json' in mimetype:  # This incorrectly checks for a specific type
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 54 =====
```
        and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
         mimetype += '; charset=%s' % charset
 
-    if mimetype:
+    if not mimetype:  # This will skip setting the Content-Type for valid mimetypes
         headers['Content-Type'] = mimetype
 
     if download is True:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if not mimetype:  # This will skip setting the Content-Type for valid mimetypes
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 55 =====
```
         mimetype += '; charset=%s' % charset
 
     if mimetype:
-        headers['Content-Type'] = mimetype
+        headers['Content-Type'] = None
 
     if download is True:
         download = os.path.basename(filename)
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = None

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 56 =====
```
         mimetype += '; charset=%s' % charset
 
     if mimetype:
-        headers['Content-Type'] = mimetype
+        headers['XXContent-TypeXX'] = mimetype
 
     if download is True:
         download = os.path.basename(filename)
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['XXContent-TypeXX'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 57 =====
```
         headers['Content-Type'] = mimetype
 
     if download is True:
-        download = os.path.basename(filename)
+        download = None
 
     if download:
         download = download.replace('"', '')
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = None

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 58 =====
```
         headers['Content-Type'] = mimetype
 
     if download is True:
-        download = os.path.basename(filename)
+        download = filename.lower()  # This converts the filename to lowercase, which may not be desired.
 
     if download:
         download = download.replace('"', '')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = filename.lower()  # This converts the filename to lowercase, which may not be desired.

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 59 =====
```
         headers['Content-Type'] = mimetype
 
     if download is True:
-        download = os.path.basename(filename)
+        download = filename.replace('/', '_')  # This replaces slashes with underscores, which is not a valid filename.
 
     if download:
         download = download.replace('"', '')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = filename.replace('/', '_')  # This replaces slashes with underscores, which is not a valid filename.

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 60 =====
```
         headers['Content-Type'] = mimetype
 
     if download is True:
-        download = os.path.basename(filename)
+        download = filename.strip()  # This removes leading and trailing whitespace, which may alter the filename incorrectly.
 
     if download:
         download = download.replace('"', '')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = filename.strip()  # This removes leading and trailing whitespace, which may alter the filename incorrectly.

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 61 =====
```
         headers['Content-Type'] = mimetype
 
     if download is True:
-        download = os.path.basename(filename)
+        download = os.path.dirname(filename)  # This incorrectly assigns the directory path instead of the filename.
 
     if download:
         download = download.replace('"', '')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.dirname(filename)  # This incorrectly assigns the directory path instead of the filename.

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 62 =====
```
     if download is True:
         download = os.path.basename(filename)
 
-    if download:
+    if download == 'yes':
         download = download.replace('"', '')
         headers['Content-Disposition'] = 'attachment; filename="%s"' % download
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download == 'yes':
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 63 =====
```
     if download is True:
         download = os.path.basename(filename)
 
-    if download:
+    if download == True:
         download = download.replace('"', '')
         headers['Content-Disposition'] = 'attachment; filename="%s"' % download
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download == True:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 64 =====
```
         download = os.path.basename(filename)
 
     if download:
-        download = download.replace('"', '')
+        download = None
         headers['Content-Disposition'] = 'attachment; filename="%s"' % download
 
     stats = os.stat(filename)
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = None
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 65 =====
```
         download = os.path.basename(filename)
 
     if download:
-        download = download.replace('"', '')
+        download = download + '_downloaded'
         headers['Content-Disposition'] = 'attachment; filename="%s"' % download
 
     stats = os.stat(filename)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download + '_downloaded'
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 66 =====
```
 
     if download:
         download = download.replace('"', '')
-        headers['Content-Disposition'] = 'attachment; filename="%s"' % download
+        headers['Content-Disposition'] = 'XXattachment; filename="%s"XX' % download
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'XXattachment; filename="%s"XX' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 67 =====
```
 
     if download:
         download = download.replace('"', '')
-        headers['Content-Disposition'] = 'attachment; filename="%s"' % download
+        headers['Content-Disposition'] = None
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = None

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 68 =====
```
 
     if download:
         download = download.replace('"', '')
-        headers['Content-Disposition'] = 'attachment; filename="%s"' % download
+        headers['XXContent-DispositionXX'] = 'attachment; filename="%s"' % download
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['XXContent-DispositionXX'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 69 =====
```
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
-    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
+    headers['Last-Modified'] = None
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
     if etag is None:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = None
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 70 =====
```
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
-    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
+    headers['Last-Modified'] = None  # Sets Last-Modified to None, which is invalid
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
     if etag is None:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = None  # Sets Last-Modified to None, which is invalid
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 71 =====
```
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
-    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
+    headers['Last-Modified'] = email.utils.formatdate(None, usegmt=True)
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
     if etag is None:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(None, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 72 =====
```
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
-    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
+    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime + 3600, usegmt=True)  # Incorrectly adds an hour to the modification time
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
     if etag is None:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime + 3600, usegmt=True)  # Incorrectly adds an hour to the modification time
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 73 =====
```
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
-    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
+    headers['Last-Modified'] = email.utils.formatdate(time.time(), usegmt=True)  # Uses current time instead of file modification time
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
     if etag is None:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(time.time(), usegmt=True)  # Uses current time instead of file modification time
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 74 =====
```
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
-    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
+    headers['Last-Modified'] = email.utils.formatdate(usegmt=True)
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
     if etag is None:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 75 =====
```
 
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
-    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
+    headers['XXLast-ModifiedXX'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
     if etag is None:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['XXLast-ModifiedXX'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 76 =====
```
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
     headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
-    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
+    headers['Date'] = "Invalid Date Format"  # Incorrect: Sets a string that does not conform to the date format
 
     if etag is None:
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = "Invalid Date Format"  # Incorrect: Sets a string that does not conform to the date format

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 77 =====
```
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
     headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
-    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
+    headers['Date'] = None
 
     if etag is None:
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = None

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 78 =====
```
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
     headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
-    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
+    headers['Date'] = email.utils.formatdate(time.time() + 3600, usegmt=True)  # Incorrect: Sets the date to one hour in the future
 
     if etag is None:
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time() + 3600, usegmt=True)  # Incorrect: Sets the date to one hour in the future

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 79 =====
```
     stats = os.stat(filename)
     headers['Content-Length'] = clen = stats.st_size
     headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
-    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
+    headers['XXDateXX'] = email.utils.formatdate(time.time(), usegmt=True)
 
     if etag is None:
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['XXDateXX'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 80 =====
```
     headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
-    if etag is None:
+    if etag == "":  # This will incorrectly treat an empty string as a valid ETag
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                    clen, filename)
         etag = hashlib.sha1(tob(etag)).hexdigest()
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag == "":  # This will incorrectly treat an empty string as a valid ETag
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 81 =====
```
     headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
-    if etag is None:
+    if etag == "invalid":  # This will only check for a specific invalid value, ignoring valid cases
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                    clen, filename)
         etag = hashlib.sha1(tob(etag)).hexdigest()
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag == "invalid":  # This will only check for a specific invalid value, ignoring valid cases
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 82 =====
```
     headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
-    if etag is None:
+    if etag is not None:
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                    clen, filename)
         etag = hashlib.sha1(tob(etag)).hexdigest()
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is not None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 83 =====
```
     headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
-    if etag is None:
+    if etag is not None:  # This will always execute the ETag handling, even if it's not set
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                    clen, filename)
         etag = hashlib.sha1(tob(etag)).hexdigest()
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is not None:  # This will always execute the ETag handling, even if it's not set
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 84 =====
```
     headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
-    if etag is None:
+    if etag:  # This will skip the ETag handling if it exists
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                    clen, filename)
         etag = hashlib.sha1(tob(etag)).hexdigest()
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag:  # This will skip the ETag handling if it exists
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 85 =====
```
     headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
 
     if etag is None:
-        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
-                                   clen, filename)
+        etag = None
         etag = hashlib.sha1(tob(etag)).hexdigest()
 
     if etag:
@@ -105,4 +104,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = None
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 86 =====
```
     if etag is None:
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                    clen, filename)
-        etag = hashlib.sha1(tob(etag)).hexdigest()
+        etag = None
 
     if etag:
         headers['ETag'] = etag
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = None

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 87 =====
```
     if etag is None:
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                    clen, filename)
-        etag = hashlib.sha1(tob(etag)).hexdigest()
+        etag = None  # Sets etag to None, effectively removing the etag functionality
 
     if etag:
         headers['ETag'] = etag
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = None  # Sets etag to None, effectively removing the etag functionality

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 88 =====
```
     if etag is None:
         etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                    clen, filename)
-        etag = hashlib.sha1(tob(etag)).hexdigest()
+        etag = hashlib.sha1(tob(None)).hexdigest()
 
     if etag:
         headers['ETag'] = etag
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(None)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 89 =====
```
                                    clen, filename)
         etag = hashlib.sha1(tob(etag)).hexdigest()
 
-    if etag:
+    if etag == '':  # This will only check for an empty string, ignoring valid ETag values.
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag == '':  # This will only check for an empty string, ignoring valid ETag values.
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 90 =====
```
                                    clen, filename)
         etag = hashlib.sha1(tob(etag)).hexdigest()
 
-    if etag:
+    if etag is True:  # This will only evaluate to True if etag is explicitly set to the boolean True, which is likely not the intended check.
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag is True:  # This will only evaluate to True if etag is explicitly set to the boolean True, which is likely not the intended check.
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 91 =====
```
                                    clen, filename)
         etag = hashlib.sha1(tob(etag)).hexdigest()
 
-    if etag:
+    if not etag:  # This will skip the ETag check if etag is an empty string or False, leading to incorrect behavior.
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if not etag:  # This will skip the ETag check if etag is an empty string or False, leading to incorrect behavior.
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 92 =====
```
         etag = hashlib.sha1(tob(etag)).hexdigest()
 
     if etag:
-        headers['ETag'] = etag
+        headers['ETag'] = None
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = None
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 93 =====
```
         etag = hashlib.sha1(tob(etag)).hexdigest()
 
     if etag:
-        headers['ETag'] = etag
+        headers['XXETagXX'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['XXETagXX'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 94 =====
```
 
     if etag:
         headers['ETag'] = etag
-        check = getenv('HTTP_IF_NONE_MATCH')
+        check = None
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = None
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 95 =====
```
 
     if etag:
         headers['ETag'] = etag
-        check = getenv('HTTP_IF_NONE_MATCH')
+        check = getenv('HTTP_IF_MODIFIED_SINCE')
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_MODIFIED_SINCE')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 96 =====
```
 
     if etag:
         headers['ETag'] = etag
-        check = getenv('HTTP_IF_NONE_MATCH')
+        check = getenv('HTTP_IF_NONE_MATCHED')
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCHED')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 97 =====
```
 
     if etag:
         headers['ETag'] = etag
-        check = getenv('HTTP_IF_NONE_MATCH')
+        check = getenv('XXHTTP_IF_NONE_MATCHXX')
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('XXHTTP_IF_NONE_MATCHXX')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 98 =====
```
 
     if etag:
         headers['ETag'] = etag
-        check = getenv('HTTP_IF_NONE_MATCH')
+        check = getenv('http_if_none_match')
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('http_if_none_match')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 99 =====
```
 
     if etag:
         headers['ETag'] = etag
-        check = getenv('HTTP_IF_NONE_MATCH')
+        check = getenv(None)
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv(None)
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 100 =====
```
     if etag:
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
-        if check and check == etag:
+        if check and check != etag:
             return HTTPResponse(status=304, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check != etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 101 =====
```
     if etag:
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
-        if check and check == etag:
+        if check and check != etag:
             return HTTPResponse(status=304, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check != etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 102 =====
```
     if etag:
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
-        if check and check == etag:
+        if check and check < etag:
             return HTTPResponse(status=304, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check < etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 103 =====
```
     if etag:
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
-        if check and check == etag:
+        if check and check is etag:
             return HTTPResponse(status=304, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check is etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 104 =====
```
     if etag:
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
-        if check and check == etag:
+        if check or check == etag:
             return HTTPResponse(status=304, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check or check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 105 =====
```
     if etag:
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
-        if check and check == etag:
+        if check or check == etag:
             return HTTPResponse(status=304, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check or check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 106 =====
```
     if etag:
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
-        if check and check == etag:
+        if not check or check == etag:
             return HTTPResponse(status=304, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if not check or check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 107 =====
```
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(**headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(**headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 108 =====
```
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=200, **headers)  # Incorrect status code for not modified
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=200, **headers)  # Incorrect status code for not modified

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 109 =====
```
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=304, )
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, )

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 110 =====
```
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=305, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=305, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 111 =====
```
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=404, **headers)  # Incorrectly indicates resource not found
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=404, **headers)  # Incorrectly indicates resource not found

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 112 =====
```
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=500, body="Internal Server Error", **headers)  # Misleading error response
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=500, body="Internal Server Error", **headers)  # Misleading error response

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 113 =====
```
         headers['ETag'] = etag
         check = getenv('HTTP_IF_NONE_MATCH')
         if check and check == etag:
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=None, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=None, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 114 =====
```
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
 
-    ims = getenv('HTTP_IF_MODIFIED_SINCE')
+    ims = None
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = None
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 115 =====
```
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
 
-    ims = getenv('HTTP_IF_MODIFIED_SINCE')
+    ims = getenv('HTTP_IF_NONE_MATCH')
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_NONE_MATCH')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 116 =====
```
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
 
-    ims = getenv('HTTP_IF_MODIFIED_SINCE')
+    ims = getenv('XXHTTP_IF_MODIFIED_SINCEXX')
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('XXHTTP_IF_MODIFIED_SINCEXX')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 117 =====
```
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
 
-    ims = getenv('HTTP_IF_MODIFIED_SINCE')
+    ims = getenv('http_if_modified_since')
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('http_if_modified_since')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 118 =====
```
         if check and check == etag:
             return HTTPResponse(status=304, **headers)
 
-    ims = getenv('HTTP_IF_MODIFIED_SINCE')
+    ims = getenv(None)
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv(None)
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 119 =====
```
             return HTTPResponse(status=304, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
-    if ims:
+    if ims == '':  # This will only check if ims is an empty string, missing valid date checks
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims == '':  # This will only check if ims is an empty string, missing valid date checks
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 120 =====
```
             return HTTPResponse(status=304, **headers)
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
-    if ims:
+    if ims is True:  # This will incorrectly check for a boolean True instead of a valid timestamp
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims is True:  # This will incorrectly check for a boolean True instead of a valid timestamp
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 121 =====
```
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
-        ims = parse_date(ims.split(";")[0].strip())
+        ims = None
         if ims is not None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = None
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 122 =====
```
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
-        ims = parse_date(ims.split(";")[0].strip())
+        ims = parse_date(None)
         if ims is not None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(None)
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 123 =====
```
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
-        ims = parse_date(ims.split(";")[0].strip())
+        ims = parse_date(ims.split(";")[0].replace(" ", ""))  # This removes all spaces, which could alter valid date formats.
         if ims is not None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].replace(" ", ""))  # This removes all spaces, which could alter valid date formats.
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 124 =====
```
 
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
-        ims = parse_date(ims.split(";")[0].strip())
+        ims = parse_date(ims.split(None)[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(None)[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 125 =====
```
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
-        if ims is not None and ims >= int(stats.st_mtime):
+        if ims is None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 126 =====
```
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
-        if ims is not None and ims >= int(stats.st_mtime):
+        if ims is None and ims >= int(stats.st_mtime):  # Incorrect condition
             return HTTPResponse(status=304, **headers)
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is None and ims >= int(stats.st_mtime):  # Incorrect condition
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 127 =====
```
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
-        if ims is not None and ims >= int(stats.st_mtime):
+        if ims is None or ims < int(stats.st_mtime):  # Incorrect logic
             return HTTPResponse(status=304, **headers)
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is None or ims < int(stats.st_mtime):  # Incorrect logic
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 128 =====
```
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
-        if ims is not None and ims >= int(stats.st_mtime):
+        if ims is not None and ims <= int(stats.st_mtime):  # Incorrect comparison
             return HTTPResponse(status=304, **headers)
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims <= int(stats.st_mtime):  # Incorrect comparison
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 129 =====
```
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
-        if ims is not None and ims >= int(stats.st_mtime):
+        if ims is not None and ims == int(stats.st_mtime):  # Only checks for equality
             return HTTPResponse(status=304, **headers)
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims == int(stats.st_mtime):  # Only checks for equality
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 130 =====
```
     ims = getenv('HTTP_IF_MODIFIED_SINCE')
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
-        if ims is not None and ims >= int(stats.st_mtime):
+        if ims is not None or ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None or ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 131 =====
```
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(**headers)
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(**headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 132 =====
```
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=200, **headers)  # Incorrect status code for not modified
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=200, **headers)  # Incorrect status code for not modified

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 133 =====
```
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=304, )
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, )

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 134 =====
```
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=305, **headers)
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=305, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 135 =====
```
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=400, body="Bad Request", **headers)  # Incorrectly indicates a bad request
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=400, body="Bad Request", **headers)  # Incorrectly indicates a bad request

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 136 =====
```
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=403, **headers)  # Incorrectly indicates forbidden access
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=403, **headers)  # Incorrectly indicates forbidden access

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 137 =====
```
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=404, **headers)  # Incorrectly indicates resource not found
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=404, **headers)  # Incorrectly indicates resource not found

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 138 =====
```
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=500, **headers)  # Incorrectly indicates a server error
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=500, **headers)  # Incorrectly indicates a server error

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 139 =====
```
     if ims:
         ims = parse_date(ims.split(";")[0].strip())
         if ims is not None and ims >= int(stats.st_mtime):
-            return HTTPResponse(status=304, **headers)
+            return HTTPResponse(status=None, **headers)
 
     body = '' if request.method == 'HEAD' else open(filename, 'rb')
 
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=None, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 140 =====
```
         if ims is not None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
 
-    body = '' if request.method == 'HEAD' else open(filename, 'rb')
+    body = '' if request.method != 'HEAD' else open(filename, 'rb')
 
     headers["Accept-Ranges"] = "bytes"
     range_header = getenv('HTTP_RANGE')
@@ -105,4 +105,4 @@         headers["Content-Length"] = str(rlen)
         if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
         return HTTPResponse(body, status=206, **headers)
-    return HTTPResponse(body, **headers)+    return HTTPResponse(body, **headers)
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method != 'HEAD' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)

```
===== 141 =====
```
         if ims is not None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
 
-    body = '' if request.method == 'HEAD' else open(filename, 'rb')
+    body = '' if request.method == 'GET' else open(filename, 'rb')
 
     headers["Accept-Ranges"] = "bytes"
     range_header = getenv('HTTP_RANGE')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'GET' else open(filename, 'rb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
===== 142 =====
```
         if ims is not None and ims >= int(stats.st_mtime):
             return HTTPResponse(status=304, **headers)
 
-    body = '' if request.method == 'HEAD' else open(filename, 'rb')
+    body = '' if request.method == 'HEAD' else open(filename, 'wb')
 
     headers["Accept-Ranges"] = "bytes"
     range_header = getenv('HTTP_RANGE')
```
```
def static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None,
                headers=None):
    """ Open a file in a safe way and return an instance of :exc:`HTTPResponse`
        that can be sent back to the client.

        :param filename: Name or path of the file to send, relative to ``root``.
        :param root: Root path for file lookups. Should be an absolute directory
            path.
        :param mimetype: Provide the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset for files with a ``text/*`` mime-type.
            (default: UTF-8)
        :param etag: Provide a pre-computed ETag header. If set to ``False``,
            ETag handling is disabled. (default: auto-generate ETag header)
        :param headers: Additional headers dict to add to the response.

        While checking user input is always a good idea, this function provides
        additional protection against malicious ``filename`` parameters from
        breaking out of the ``root`` directory and leaking sensitive information
        to an attacker.

        Read-protected files or files outside of the ``root`` directory are
        answered with ``403 Access Denied``. Missing files result in a
        ``404 Not Found`` response. Conditional requests (``If-Modified-Since``,
        ``If-None-Match``) are answered with ``304 Not Modified`` whenever
        possible. ``HEAD`` and ``Range`` requests (used by download managers to
        check or continue partial downloads) are also handled automatically.
    """

    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = headers.copy() if headers else {}
    getenv = request.environ.get

    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")

    if mimetype is True:
        name = download if isinstance(download, str) else filename
        mimetype, encoding = mimetypes.guess_type(name)
        if encoding == 'gzip':
            mimetype = 'application/gzip'
        elif encoding:  # e.g. bzip2 -> application/x-bzip2
            mimetype = 'application/x-' + encoding

    if charset and mimetype and 'charset=' not in mimetype \
       and (mimetype[:5] == 'text/' or mimetype == 'application/javascript'):
        mimetype += '; charset=%s' % charset

    if mimetype:
        headers['Content-Type'] = mimetype

    if download is True:
        download = os.path.basename(filename)

    if download:
        download = download.replace('"', '')
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)

    if etag is None:
        etag = '%d:%d:%d:%d:%s' % (stats.st_dev, stats.st_ino, stats.st_mtime,
                                   clen, filename)
        etag = hashlib.sha1(tob(etag)).hexdigest()

    if etag:
        headers['ETag'] = etag
        check = getenv('HTTP_IF_NONE_MATCH')
        if check and check == etag:
            return HTTPResponse(status=304, **headers)

    ims = getenv('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else open(filename, 'wb')

    headers["Accept-Ranges"] = "bytes"
    range_header = getenv('HTTP_RANGE')
    if range_header:
        ranges = list(parse_range_header(range_header, clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        rlen = end - offset
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(rlen)
        if body: body = _closeiter(_rangeiter(body, offset, rlen), body.close)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
```
