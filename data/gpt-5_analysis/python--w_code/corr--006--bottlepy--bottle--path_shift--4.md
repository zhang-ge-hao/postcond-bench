https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L3037-L3065
```
@icontract.snapshot(lambda script_name: ([] if script_name.strip('/') == '' else script_name.strip('/').split('/')), name="script_tokens")
@icontract.snapshot(lambda path_info: ([] if path_info.strip('/') == '' else path_info.strip('/').split('/')), name="path_tokens")
@icontract.snapshot(lambda path_info: path_info.endswith('/'), name="path_endswith")
@icontract.ensure(lambda result, script_name, path_info, shift: (shift != 0) or (result[0] == script_name and result[1] == path_info))
@icontract.ensure(lambda result, shift: (shift == 0) or (result[0].startswith('/') and result[1].startswith('/')))
@icontract.ensure(lambda OLD, shift: (shift == 0) or ((shift > 0 and shift <= len(OLD.path_tokens)) or (shift < 0 and -shift <= len(OLD.script_tokens))))
@icontract.ensure(lambda result, OLD: (([] if result[0].strip('/') == '' else result[0].strip('/').split('/')) + ([] if result[1].strip('/') == '' else result[1].strip('/').split('/'))) == (OLD.script_tokens + OLD.path_tokens))
@icontract.ensure(lambda result, OLD, shift: (shift == 0) or (len([] if result[0].strip('/') == '' else result[0].strip('/').split('/')) == len(OLD.script_tokens) + shift))
@icontract.ensure(lambda result, OLD, shift: (shift <= 0) or ((([] if result[0].strip('/') == '' else result[0].strip('/').split('/')) == (OLD.script_tokens + OLD.path_tokens[:shift])) and (([] if result[1].strip('/') == '' else result[1].strip('/').split('/')) == (OLD.path_tokens[shift:]))))
@icontract.ensure(lambda result, OLD, shift: (shift >= 0) or ((([] if result[0].strip('/') == '' else result[0].strip('/').split('/')) == (OLD.script_tokens[:shift])) and (([] if result[1].strip('/') == '' else result[1].strip('/').split('/')) == (OLD.script_tokens[shift:] + OLD.path_tokens))))
@icontract.ensure(lambda result, OLD, shift: (shift == 0 and (result[1].endswith('/') == OLD.path_endswith)) or (shift != 0 and (result[1].endswith('/') == (OLD.path_endswith and len([] if result[1].strip('/') == '' else result[1].strip('/').split('/')) > 0))))
@icontract.ensure(lambda result, shift: (shift == 0) or ((result[0] == '/') or (not result[0].endswith('/'))))
```
```
Hallucination.

Wrong Post-cond:

@icontract.ensure(lambda result, OLD, shift: (shift == 0 and (result[1].endswith('/') == OLD.path_endswith)) or (shift != 0 and (result[1].endswith('/') == (OLD.path_endswith and len([] if result[1].strip('/') == '' else result[1].strip('/').split('/')) > 0))))

(shift != 0 and (result[1].endswith('/') == (OLD.path_endswith and len([] if result[1].strip('/') == '' else result[1].strip('/').split('/')) > 0)))

But when:

path_info was '/a/b/c/d'
script_name was '/'
OLD.path_endswith is False

result was ('/a/b/c/d', '/')
result[1] was '/'
result[1].endswith('/') is True

So there is a situation that when new_path_info is root, it has to end with "/". But path_info can not be ended with "/".
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
