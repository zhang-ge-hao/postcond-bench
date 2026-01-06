https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/sysctl.py#L72-L92
```
@icontract.snapshot(lambda proc_data: dict(proc_data), name="old_proc_data")
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda result, proc_data: result is not proc_data)
@icontract.ensure(lambda result: all(isinstance(k, str) for k in result.keys()))
@icontract.ensure(lambda result: all(isinstance(v, (str, int, float)) for v in result.values()))
@icontract.ensure(lambda result, proc_data: set(result.keys()) == set(proc_data.keys()))
@icontract.ensure(lambda OLD, proc_data: proc_data == OLD.old_proc_data)
```
```
Hallucination.

@icontract.ensure(lambda result, proc_data: result is not proc_data)

This postcond needs return value is not the same object to inputted proc_data. But no evidence shows this feature and in practice it is.
```
icontract_fail
```
@icontract.snapshot(lambda proc_data: proc_data.copy())
@icontract.ensure(lambda OLD, proc_data: set(proc_data.keys()) == set(OLD.proc_data.keys()))
@icontract.ensure(lambda OLD, proc_data: all((not OLD.proc_data[k].lstrip('+-').isdigit()) or (isinstance(proc_data[k], int) and proc_data[k] == int(OLD.proc_data[k])) for k in proc_data))
@icontract.ensure(lambda OLD, proc_data: all((not (lambda s: (s.count('.') == 1 and (lambda a,b: a.isdigit() and b.isdigit())(*s.split('.',1))))(OLD.proc_data[k].lstrip('+-'))) or (isinstance(proc_data[k], float) and proc_data[k] == float(OLD.proc_data[k])) for k in proc_data))
@icontract.ensure(lambda OLD, proc_data: all(( (not OLD.proc_data[k].lstrip('+-').isdigit()) and (not (lambda s: (s.count('.') == 1 and (lambda a,b: a.isdigit() and b.isdigit())(*s.split('.',1))))(OLD.proc_data[k].lstrip('+-')) ) ) <= (proc_data[k] == OLD.proc_data[k]) for k in proc_data))
```
