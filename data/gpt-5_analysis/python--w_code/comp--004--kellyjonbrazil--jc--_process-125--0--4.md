https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/sysctl.py#L72-L92
```
@icontract.snapshot(lambda proc_data: dict(proc_data))
@icontract.ensure(lambda result, proc_data: result is proc_data)
@icontract.ensure(lambda OLD, proc_data: set(proc_data.keys()) == set(OLD.proc_data.keys()))
@icontract.ensure(lambda OLD, proc_data: all((proc_data[k] == OLD.proc_data[k]) or isinstance(proc_data[k], (int, float)) for k in proc_data))
@icontract.ensure(lambda OLD, proc_data: all((not isinstance(OLD.proc_data[k], str)) or (not OLD.proc_data[k].strip().lstrip("+-").isdigit()) or (isinstance(proc_data[k], int) and proc_data[k] == int(OLD.proc_data[k])) for k in proc_data))
@icontract.ensure(lambda OLD, proc_data: all((not isinstance(OLD.proc_data[k], str)) or (not (('.' in OLD.proc_data[k].strip().lstrip('+-')) and OLD.proc_data[k].strip().lstrip('+-').replace('.', '', 1).isdigit() and not OLD.proc_data[k].strip().lstrip('+-').isdigit())) or (isinstance(proc_data[k], float) and proc_data[k] == float(OLD.proc_data[k])) for k in proc_data))
```
```
Corner case missed.

Does not considered proc_data[key] == "" situation.
```
passed
```
@icontract.snapshot(lambda proc_data: proc_data.copy())
@icontract.ensure(lambda OLD, proc_data: set(proc_data.keys()) == set(OLD.proc_data.keys()))
@icontract.ensure(lambda OLD, proc_data: all((not OLD.proc_data[k].lstrip('+-').isdigit()) or (isinstance(proc_data[k], int) and proc_data[k] == int(OLD.proc_data[k])) for k in proc_data))
@icontract.ensure(lambda OLD, proc_data: all((not (lambda s: (s.count('.') == 1 and (lambda a,b: a.isdigit() and b.isdigit())(*s.split('.',1))))(OLD.proc_data[k].lstrip('+-'))) or (isinstance(proc_data[k], float) and proc_data[k] == float(OLD.proc_data[k])) for k in proc_data))
@icontract.ensure(lambda OLD, proc_data: all(( (not OLD.proc_data[k].lstrip('+-').isdigit()) and (not (lambda s: (s.count('.') == 1 and (lambda a,b: a.isdigit() and b.isdigit())(*s.split('.',1))))(OLD.proc_data[k].lstrip('+-')) ) ) <= (proc_data[k] == OLD.proc_data[k]) for k in proc_data))
```
===== 4 =====
failed
```
             proc_data[key] = int(proc_data[key])
         except (ValueError):
             try:
-                proc_data[key] = float(proc_data[key])
+                proc_data[key] = float(proc_data[key]) if proc_data[key] else 0.0  # Converts to float but defaults to 0.0 if the value is falsy
             except (ValueError):
                 pass
     return proc_data
```
```
def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    for key in proc_data:
        try:
            proc_data[key] = int(proc_data[key])
        except (ValueError):
            try:
                proc_data[key] = float(proc_data[key]) if proc_data[key] else 0.0  # Converts to float but defaults to 0.0 if the value is falsy
            except (ValueError):
                pass
    return proc_data
```
