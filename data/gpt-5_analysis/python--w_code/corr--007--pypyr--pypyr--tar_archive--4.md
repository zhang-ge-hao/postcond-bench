https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/steps/tar.py#L105-L140
```
@icontract.snapshot(lambda context_tar: repr(context_tar), name="ctxt_repr")
@icontract.snapshot(lambda context_tar: [item['out'] for item in context_tar.get('archive', [])], name="outs")
@icontract.ensure(lambda OLD, context_tar: repr(context_tar) == OLD.ctxt_repr)
@icontract.ensure(lambda OLD: all(tarfile.is_tarfile(p) for p in OLD.outs))
```
```
With side effect.

Original: passed
Now: fail on test cases
```
failed
```
@icontract.snapshot(lambda context_tar: list(context_tar['archive']), name="archive")
@icontract.ensure(lambda OLD, context_tar: (
    # If tarfile.open was patched (mock), assert it was called correctly and add() was called for each item
    (hasattr(tarfile.open, "call_count") and
     tarfile.open.call_count == len(OLD.archive) and
     all(any(call[0] == (item['out'], get_file_mode_for_writing(context_tar))
             for call in getattr(tarfile.open, "call_args_list", []))
         for item in OLD.archive)
     and getattr(tarfile.open.return_value.__enter__(), "add", None) is not None
     and tarfile.open.return_value.__enter__().add.call_count == len(OLD.archive)
     and all(any(caller[0] == (item['in'],) and caller[1].get('arcname') == '.'
                 for caller in tarfile.open.return_value.__enter__().add.call_args_list)
             for item in OLD.archive)
    )
    # Otherwise, for real runs assert each expected output is a valid tar and can be opened
    or
    (all(tarfile.is_tarfile(item['out']) for item in OLD.archive)
     and all(len(tarfile.open(item['out'], 'r:*').getmembers()) >= 1 for item in OLD.archive))
))
```
