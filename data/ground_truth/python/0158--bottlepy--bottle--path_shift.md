https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L3037-L3065
```
@icontract.ensure(
    lambda result, script_name, path_info, shift:
        not (shift == 0) or
        result == (script_name, path_info)
)
@icontract.ensure(
    lambda result, script_name, path_info, shift:
        not (shift > 0) or
        result == (
            '/' + '/'.join(
                (
                    [] if script_name.strip('/').split('/')[0] == ''
                    else script_name.strip('/').split('/')
                )
                +
                (
                    [] if path_info.strip('/').split('/')[0] == ''
                    else path_info.strip('/').split('/')
                )[:shift]
            ),
            (
                '/' + '/'.join(
                    (
                        [] if path_info.strip('/').split('/')[0] == ''
                        else path_info.strip('/').split('/')
                    )[shift:]
                )
                + (
                    '/'
                    if path_info.endswith('/')
                    and (
                        [] if path_info.strip('/').split('/')[0] == ''
                        else path_info.strip('/').split('/')
                    )[shift:]
                    else ''
                )
            )
        )
)
@icontract.ensure(
    lambda result, script_name, path_info, shift:
        not (shift < 0) or
        result == (
            '/' + '/'.join(
                (
                    [] if script_name.strip('/').split('/')[0] == ''
                    else script_name.strip('/').split('/')
                )[:shift]
            ),
            (
                '/' + '/'.join(
                    (
                        [] if script_name.strip('/').split('/')[0] == ''
                        else script_name.strip('/').split('/')
                    )[shift:]
                    +
                    (
                        [] if path_info.strip('/').split('/')[0] == ''
                        else path_info.strip('/').split('/')
                    )
                )
                + (
                    '/'
                    if path_info.endswith('/')
                    and (
                        (
                            [] if script_name.strip('/').split('/')[0] == ''
                            else script_name.strip('/').split('/')
                        )[shift:]
                        +
                        (
                            [] if path_info.strip('/').split('/')[0] == ''
                            else path_info.strip('/').split('/')
                        )
                    )
                    else ''
                )
            )
        )
)
```
```
@icontract.snapshot(lambda script_name: script_name, name="old_script")
@icontract.snapshot(lambda path_info: path_info, name="old_path")
@icontract.snapshot(lambda shift: shift, name="old_shift")
@icontract.snapshot(lambda script_name: [] if script_name.strip('/') == '' else script_name.strip('/').split('/'), name="old_script_segments")
@icontract.snapshot(lambda path_info: [] if path_info.strip('/') == '' else path_info.strip('/').split('/'), name="old_path_segments")
@icontract.snapshot(lambda path_info: path_info.endswith('/'), name="old_path_ends_slash")
@icontract.ensure(lambda result, OLD: result == (OLD.old_script, OLD.old_path) if OLD.old_shift == 0 else True)
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], str) and isinstance(result[1], str))
@icontract.ensure(lambda result: result[0].startswith('/') and result[1].startswith('/'))
@icontract.ensure(lambda result: not (result[0].endswith('/') and result[0] != '/'))
@icontract.ensure(lambda result: not result[1].endswith('//'))
@icontract.ensure(lambda result, OLD: (OLD.old_script_segments + OLD.old_path_segments) == ( [] if result[0].strip('/') == '' else result[0].strip('/').split('/') ) + ( [] if result[1].strip('/') == '' else result[1].strip('/').split('/') ))
@icontract.ensure(lambda result, OLD: (result[1].endswith('/')) == (([] if result[1].strip('/') == '' else result[1].strip('/').split('/')) == [] or (OLD.old_path_ends_slash and ([] if result[1].strip('/') == '' else result[1].strip('/').split('/')) != [])))
```
[2, 3, 6, 7, 15, 16, 17, 19, 20, 21, 29, 36]
===== 2 =====
```
           change the shift direction. (default: 1)
     """
     if shift == 0: return script_name, path_info
-    pathlist = path_info.strip('/').split('/')
+    pathlist = path_info.strip('/').split('XX/XX')
     scriptlist = script_name.strip('/').split('/')
     if pathlist and pathlist[0] == '': pathlist = []
     if scriptlist and scriptlist[0] == '': scriptlist = []
@@ -26,4 +26,4 @@     new_script_name = '/' + '/'.join(scriptlist)
     new_path_info = '/' + '/'.join(pathlist)
     if path_info.endswith('/') and pathlist: new_path_info += '/'
-    return new_script_name, new_path_info+    return new_script_name, new_path_info
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('XX/XX')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info

```
===== 3 =====
```
           change the shift direction. (default: 1)
     """
     if shift == 0: return script_name, path_info
-    pathlist = path_info.strip('/').split('/')
+    pathlist = path_info.strip('/').split(None)
     scriptlist = script_name.strip('/').split('/')
     if pathlist and pathlist[0] == '': pathlist = []
     if scriptlist and scriptlist[0] == '': scriptlist = []
@@ -26,4 +26,4 @@     new_script_name = '/' + '/'.join(scriptlist)
     new_path_info = '/' + '/'.join(pathlist)
     if path_info.endswith('/') and pathlist: new_path_info += '/'
-    return new_script_name, new_path_info+    return new_script_name, new_path_info
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split(None)
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info

```
===== 6 =====
```
     """
     if shift == 0: return script_name, path_info
     pathlist = path_info.strip('/').split('/')
-    scriptlist = script_name.strip('/').split('/')
+    scriptlist = script_name.strip('/').split('XX/XX')
     if pathlist and pathlist[0] == '': pathlist = []
     if scriptlist and scriptlist[0] == '': scriptlist = []
     if 0 < shift <= len(pathlist):
@@ -26,4 +26,4 @@     new_script_name = '/' + '/'.join(scriptlist)
     new_path_info = '/' + '/'.join(pathlist)
     if path_info.endswith('/') and pathlist: new_path_info += '/'
-    return new_script_name, new_path_info+    return new_script_name, new_path_info
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('XX/XX')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info

```
===== 7 =====
```
     """
     if shift == 0: return script_name, path_info
     pathlist = path_info.strip('/').split('/')
-    scriptlist = script_name.strip('/').split('/')
+    scriptlist = script_name.strip('/').split(None)
     if pathlist and pathlist[0] == '': pathlist = []
     if scriptlist and scriptlist[0] == '': scriptlist = []
     if 0 < shift <= len(pathlist):
@@ -26,4 +26,4 @@     new_script_name = '/' + '/'.join(scriptlist)
     new_path_info = '/' + '/'.join(pathlist)
     if path_info.endswith('/') and pathlist: new_path_info += '/'
-    return new_script_name, new_path_info+    return new_script_name, new_path_info
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split(None)
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info

```
===== 15 =====
```
     pathlist = path_info.strip('/').split('/')
     scriptlist = script_name.strip('/').split('/')
     if pathlist and pathlist[0] == '': pathlist = []
-    if scriptlist and scriptlist[0] == '': scriptlist = []
+    if scriptlist and scriptlist[0] == ' ': scriptlist = []
     if 0 < shift <= len(pathlist):
         moved = pathlist[:shift]
         scriptlist = scriptlist + moved
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == ' ': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info
```
===== 16 =====
```
     pathlist = path_info.strip('/').split('/')
     scriptlist = script_name.strip('/').split('/')
     if pathlist and pathlist[0] == '': pathlist = []
-    if scriptlist and scriptlist[0] == '': scriptlist = []
+    if scriptlist and scriptlist[0] == 'XXXX': scriptlist = []
     if 0 < shift <= len(pathlist):
         moved = pathlist[:shift]
         scriptlist = scriptlist + moved
@@ -26,4 +26,4 @@     new_script_name = '/' + '/'.join(scriptlist)
     new_path_info = '/' + '/'.join(pathlist)
     if path_info.endswith('/') and pathlist: new_path_info += '/'
-    return new_script_name, new_path_info+    return new_script_name, new_path_info
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == 'XXXX': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info

```
===== 17 =====
```
     pathlist = path_info.strip('/').split('/')
     scriptlist = script_name.strip('/').split('/')
     if pathlist and pathlist[0] == '': pathlist = []
-    if scriptlist and scriptlist[0] == '': scriptlist = []
+    if scriptlist and scriptlist[0] is None: scriptlist = []
     if 0 < shift <= len(pathlist):
         moved = pathlist[:shift]
         scriptlist = scriptlist + moved
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] is None: scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info
```
===== 19 =====
```
         scriptlist = scriptlist[:shift]
     else:
         empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
-        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
+        pass  # No action taken, just skipping the shift
     new_script_name = '/' + '/'.join(scriptlist)
     new_path_info = '/' + '/'.join(pathlist)
     if path_info.endswith('/') and pathlist: new_path_info += '/'
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        pass  # No action taken, just skipping the shift
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info
```
===== 20 =====
```
         scriptlist = scriptlist[:shift]
     else:
         empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
-        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
+        print("Cannot shift. Nothing left from %s" % empty)
     new_script_name = '/' + '/'.join(scriptlist)
     new_path_info = '/' + '/'.join(pathlist)
     if path_info.endswith('/') and pathlist: new_path_info += '/'
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        print("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info
```
===== 21 =====
```
         scriptlist = scriptlist[:shift]
     else:
         empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
-        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
+        return "Cannot shift. Nothing left from %s" % empty
     new_script_name = '/' + '/'.join(scriptlist)
     new_path_info = '/' + '/'.join(pathlist)
     if path_info.endswith('/') and pathlist: new_path_info += '/'
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        return "Cannot shift. Nothing left from %s" % empty
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info
```
===== 29 =====
```
     else:
         empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
         raise AssertionError("Cannot shift. Nothing left from %s" % empty)
-    new_script_name = '/' + '/'.join(scriptlist)
+    new_script_name = None
     new_path_info = '/' + '/'.join(pathlist)
     if path_info.endswith('/') and pathlist: new_path_info += '/'
-    return new_script_name, new_path_info+    return new_script_name, new_path_info
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = None
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info

```
===== 36 =====
```
         empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
         raise AssertionError("Cannot shift. Nothing left from %s" % empty)
     new_script_name = '/' + '/'.join(scriptlist)
-    new_path_info = '/' + '/'.join(pathlist)
+    new_path_info = None
     if path_info.endswith('/') and pathlist: new_path_info += '/'
-    return new_script_name, new_path_info+    return new_script_name, new_path_info
```
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = None
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info

```
