https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L3037-L3065
```
@icontract.snapshot(lambda script_name: [] if script_name.strip('/').split('/') == [''] else script_name.strip('/').split('/'), name="script_segs")
@icontract.snapshot(lambda path_info: [] if path_info.strip('/').split('/') == [''] else path_info.strip('/').split('/'), name="path_segs")
@icontract.snapshot(lambda path_info: path_info.endswith('/'), name="path_trailing")
@icontract.ensure(lambda result, script_name, path_info, shift: (shift != 0) or (result[0] == script_name and result[1] == path_info))
@icontract.ensure(lambda OLD, shift: (shift == 0) or ((shift > 0 and shift <= len(OLD.path_segs)) or (shift < 0 and -shift <= len(OLD.script_segs))))
@icontract.ensure(lambda result: result[0].startswith('/') and result[1].startswith('/'))
@icontract.ensure(lambda result: (result[0] == '/') or (not result[0].endswith('/')))
@icontract.ensure(lambda result, OLD: result[1].endswith('/') == (OLD.path_trailing and result[1] != '/'))
@icontract.ensure(lambda result, OLD: (len([] if result[0].strip('/').split('/') == [''] else result[0].strip('/').split('/')) + len([] if result[1].strip('/').split('/') == [''] else result[1].strip('/').split('/'))) == (len(OLD.script_segs) + len(OLD.path_segs)))
@icontract.ensure(lambda result: (([] if result[1].strip('/').split('/') == [''] else result[1].strip('/').split('/')) == []) == (result[1] == '/'))
@icontract.ensure(lambda result, OLD, shift: (shift <= 0) or (([] if result[0].strip('/').split('/') == [''] else result[0].strip('/').split('/')) == OLD.script_segs + OLD.path_segs[:shift]))
@icontract.ensure(lambda result, OLD, shift: (shift <= 0) or (([] if result[1].strip('/').split('/') == [''] else result[1].strip('/').split('/')) == OLD.path_segs[shift:]))
@icontract.ensure(lambda result, OLD, shift: (shift >= 0) or (([] if result[0].strip('/').split('/') == [''] else result[0].strip('/').split('/')) == OLD.script_segs[:shift]))
@icontract.ensure(lambda result, OLD, shift: (shift >= 0) or (([] if result[1].strip('/').split('/') == [''] else result[1].strip('/').split('/')) == OLD.script_segs[shift:] + OLD.path_segs))
```
```
Hallucination.

Same to corr--006--bottlepy--bottle--path_shift--4.
```
icontract_fail
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
