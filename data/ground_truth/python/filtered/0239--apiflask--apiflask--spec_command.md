https://github.com/apiflask/apiflask/blob/13d2a1b51a7ec68fdcfb9c6250f2db107fcf359a/./src/apiflask/commands.py#L7-L54
```
🈚️

features on print
no mock util can use
```
```
@icontract.ensure(lambda expected_format, spec_format: spec_format == expected_format)
@icontract.ensure(lambda resolved_indent, indent: indent == resolved_indent)
@icontract.ensure(lambda expected_json_indent, json_indent: json_indent == expected_json_indent)
@icontract.ensure(lambda expected_format, raw_spec, spec: (isinstance(spec, str) and json.loads(spec) == raw_spec) if expected_format == 'json' else spec == raw_spec)
@icontract.ensure(lambda quiet, expected_output_str: (quiet is True) or (getattr(__import__('sys').stdout, 'getvalue', lambda: '')() is not None and expected_output_str in getattr(__import__('sys').stdout, 'getvalue')()))
@icontract.ensure(lambda expected_output_path, expected_output_str: (not expected_output_path) or (__import__('os').path.exists(expected_output_path) and expected_output_str in open(expected_output_path, 'r').read()))
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
===== 0 =====
```
 
     https://apiflask.com/openapi/#the-flask-spec-command
     """
-    spec_format = format or current_app.config['SPEC_FORMAT']
+    spec_format = None
     spec = current_app._get_spec(spec_format)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = None
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 1 =====
```
 
     https://apiflask.com/openapi/#the-flask-spec-command
     """
-    spec_format = format or current_app.config['SPEC_FORMAT']
+    spec_format = format and current_app.config['SPEC_FORMAT']
     spec = current_app._get_spec(spec_format)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format and current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 2 =====
```
     https://apiflask.com/openapi/#the-flask-spec-command
     """
     spec_format = format or current_app.config['SPEC_FORMAT']
-    spec = current_app._get_spec(spec_format)
+    spec = None
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = None
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 3 =====
```
     https://apiflask.com/openapi/#the-flask-spec-command
     """
     spec_format = format or current_app.config['SPEC_FORMAT']
-    spec = current_app._get_spec(spec_format)
+    spec = current_app._get_spec('json' if spec_format == 'yaml' else spec_format)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec('json' if spec_format == 'yaml' else spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 4 =====
```
     https://apiflask.com/openapi/#the-flask-spec-command
     """
     spec_format = format or current_app.config['SPEC_FORMAT']
-    spec = current_app._get_spec(spec_format)
+    spec = current_app._get_spec(None)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(None)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 5 =====
```
     https://apiflask.com/openapi/#the-flask-spec-command
     """
     spec_format = format or current_app.config['SPEC_FORMAT']
-    spec = current_app._get_spec(spec_format)
+    spec = current_app._get_spec(spec_format) if output else None
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format) if output else None
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 6 =====
```
     """
     spec_format = format or current_app.config['SPEC_FORMAT']
     spec = current_app._get_spec(spec_format)
-    output_path = output or current_app.config['LOCAL_SPEC_PATH']
+    output_path = None
     if indent is None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = None
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 7 =====
```
     """
     spec_format = format or current_app.config['SPEC_FORMAT']
     spec = current_app._get_spec(spec_format)
-    output_path = output or current_app.config['LOCAL_SPEC_PATH']
+    output_path = output and current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output and current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 8 =====
```
     spec_format = format or current_app.config['SPEC_FORMAT']
     spec = current_app._get_spec(spec_format)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
-    if indent is None:
+    if indent == 1:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent == 1:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 9 =====
```
     spec_format = format or current_app.config['SPEC_FORMAT']
     spec = current_app._get_spec(spec_format)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
-    if indent is None:
+    if indent is False:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is False:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 10 =====
```
     spec_format = format or current_app.config['SPEC_FORMAT']
     spec = current_app._get_spec(spec_format)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
-    if indent is None:
+    if indent is True:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is True:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 11 =====
```
     spec_format = format or current_app.config['SPEC_FORMAT']
     spec = current_app._get_spec(spec_format)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
-    if indent is None:
+    if indent is not None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is not None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 12 =====
```
     spec_format = format or current_app.config['SPEC_FORMAT']
     spec = current_app._get_spec(spec_format)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
-    if indent is None:
+    if indent is not None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
 
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is not None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 13 =====
```
     spec = current_app._get_spec(spec_format)
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
-        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
+        indent = None
     json_indent = None if indent == 0 else indent
 
     if spec_format == 'json':
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = None
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 14 =====
```
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
-    json_indent = None if indent == 0 else indent
+    json_indent = None
 
     if spec_format == 'json':
         spec = json.dumps(spec, indent=json_indent)
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 15 =====
```
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
-    json_indent = None if indent == 0 else indent
+    json_indent = None if indent != 0 else indent
 
     if spec_format == 'json':
         spec = json.dumps(spec, indent=json_indent)
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent != 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 16 =====
```
     output_path = output or current_app.config['LOCAL_SPEC_PATH']
     if indent is None:
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
-    json_indent = None if indent == 0 else indent
+    json_indent = None if indent == 1 else indent
 
     if spec_format == 'json':
         spec = json.dumps(spec, indent=json_indent)
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 1 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 17 =====
```
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
 
-    if spec_format == 'json':
+    if not spec_format:  # Checks for empty format instead of specific format
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if not spec_format:  # Checks for empty format instead of specific format
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 18 =====
```
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
 
-    if spec_format == 'json':
+    if spec_format != 'json':
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format != 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 19 =====
```
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
 
-    if spec_format == 'json':
+    if spec_format != 'json':  # Negation introduces a bug
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format != 'json':  # Negation introduces a bug
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 20 =====
```
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
 
-    if spec_format == 'json':
+    if spec_format == 'JSON':
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'JSON':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 21 =====
```
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
 
-    if spec_format == 'json':
+    if spec_format == 'XXjsonXX':
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'XXjsonXX':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 22 =====
```
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
 
-    if spec_format == 'json':
+    if spec_format == 'json' and output_path is None:  # Conditional logic flaw
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json' and output_path is None:  # Conditional logic flaw
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 23 =====
```
         indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
     json_indent = None if indent == 0 else indent
 
-    if spec_format == 'json':
+    if spec_format == 'yaml':  # Incorrect format check
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'yaml':  # Incorrect format check
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 24 =====
```
     json_indent = None if indent == 0 else indent
 
     if spec_format == 'json':
-        spec = json.dumps(spec, indent=json_indent)
+        spec = None
 
     # output to stdout
     if not quiet:
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = None

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 25 =====
```
     json_indent = None if indent == 0 else indent
 
     if spec_format == 'json':
-        spec = json.dumps(spec, indent=json_indent)
+        spec = json.dumps(None, indent=json_indent)
 
     # output to stdout
     if not quiet:
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(None, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 26 =====
```
     json_indent = None if indent == 0 else indent
 
     if spec_format == 'json':
-        spec = json.dumps(spec, indent=json_indent)
+        spec = json.dumps(spec)  # Missing indentation parameter
 
     # output to stdout
     if not quiet:
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec)  # Missing indentation parameter

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 27 =====
```
     json_indent = None if indent == 0 else indent
 
     if spec_format == 'json':
-        spec = json.dumps(spec, indent=json_indent)
+        spec = json.dumps(spec, )
 
     # output to stdout
     if not quiet:
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, )

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 28 =====
```
     json_indent = None if indent == 0 else indent
 
     if spec_format == 'json':
-        spec = json.dumps(spec, indent=json_indent)
+        spec = json.dumps(spec, indent='  ')  # Indentation provided as a string instead of an integer
 
     # output to stdout
     if not quiet:
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent='  ')  # Indentation provided as a string instead of an integer

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 29 =====
```
     json_indent = None if indent == 0 else indent
 
     if spec_format == 'json':
-        spec = json.dumps(spec, indent=json_indent)
+        spec = json.dumps(spec, indent=0)  # Indentation set to 0, resulting in no formatting
 
     # output to stdout
     if not quiet:
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=0)  # Indentation set to 0, resulting in no formatting

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 30 =====
```
     json_indent = None if indent == 0 else indent
 
     if spec_format == 'json':
-        spec = json.dumps(spec, indent=json_indent)
+        spec = json.dumps(spec, indent=None)
 
     # output to stdout
     if not quiet:
@@ -45,4 +45,4 @@     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=None)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 31 =====
```
     json_indent = None if indent == 0 else indent
 
     if spec_format == 'json':
-        spec = json.dumps(spec, indent=json_indent)
+        spec = json.dumps(spec, indent=None)  # Passing None as the indentation, which is not valid
 
     # output to stdout
     if not quiet:
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=None)  # Passing None as the indentation, which is not valid

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 32 =====
```
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
-    if not quiet:
+    if output_path is None:  # This will prevent output to stdout if no output path is provided, which is not the intended logic.
         click.echo(spec)
 
     # output to local file
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if output_path is None:  # This will prevent output to stdout if no output path is provided, which is not the intended logic.
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 33 =====
```
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
-    if not quiet:
+    if quiet:
         click.echo(spec)
 
     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 34 =====
```
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
-    if not quiet:
+    if quiet:  # This will suppress output when the flag is set, which is the opposite of the intended behavior.
         click.echo(spec)
 
     # output to local file
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if quiet:  # This will suppress output when the flag is set, which is the opposite of the intended behavior.
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 35 =====
```
         spec = json.dumps(spec, indent=json_indent)
 
     # output to stdout
-    if not quiet:
+    if spec_format == 'yaml':  # This condition is unrelated to the quiet flag and will not control the output behavior correctly.
         click.echo(spec)
 
     # output to local file
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if spec_format == 'yaml':  # This condition is unrelated to the quiet flag and will not control the output behavior correctly.
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 36 =====
```
 
     # output to stdout
     if not quiet:
-        click.echo(spec)
+        click.echo(None)
 
     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(None)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)

```
===== 37 =====
```
         click.echo(spec)
 
     # output to local file
-    if output_path:
+    if not output_path:
         with open(output_path, 'w') as f:
             click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if not output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 38 =====
```
         click.echo(spec)
 
     # output to local file
-    if output_path:
+    if output_path == '':
         with open(output_path, 'w') as f:
             click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path == '':
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 39 =====
```
         click.echo(spec)
 
     # output to local file
-    if output_path:
+    if output_path and len(output_path) > 0:
         with open(output_path, 'w') as f:
             click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path and len(output_path) > 0:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 40 =====
```
         click.echo(spec)
 
     # output to local file
-    if output_path:
+    if output_path and output_path != current_app.config['LOCAL_SPEC_PATH']:
         with open(output_path, 'w') as f:
             click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path and output_path != current_app.config['LOCAL_SPEC_PATH']:
        with open(output_path, 'w') as f:
            click.echo(spec, file=f)
```
===== 41 =====
```
 
     # output to local file
     if output_path:
-        with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+        with open('w') as f:
+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open('w') as f:
            click.echo(spec, file=f)

```
===== 42 =====
```
 
     # output to local file
     if output_path:
-        with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+        with open(None, 'w') as f:
+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(None, 'w') as f:
            click.echo(spec, file=f)

```
===== 43 =====
```
 
     # output to local file
     if output_path:
-        with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+        with open(output_path, 'W') as f:
+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'W') as f:
            click.echo(spec, file=f)

```
===== 44 =====
```
 
     # output to local file
     if output_path:
-        with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+        with open(output_path, 'XXwXX') as f:
+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'XXwXX') as f:
            click.echo(spec, file=f)

```
===== 45 =====
```
 
     # output to local file
     if output_path:
-        with open(output_path, 'w') as f:
+        with open(output_path, 'r') as f:  # Tries to read from the file instead of writing, leading to a logic error
             click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'r') as f:  # Tries to read from the file instead of writing, leading to a logic error
            click.echo(spec, file=f)
```
===== 46 =====
```
 
     # output to local file
     if output_path:
-        with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+        with open(output_path, ) as f:
+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, ) as f:
            click.echo(spec, file=f)

```
===== 47 =====
```
 
     # output to local file
     if output_path:
-        with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+        with open(output_path, None) as f:
+            click.echo(spec, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, None) as f:
            click.echo(spec, file=f)

```
===== 48 =====
```
     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(None, file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(None, file=f)

```
===== 49 =====
```
     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(file=f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(file=f)

```
===== 50 =====
```
     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, )
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, )

```
===== 51 =====
```
     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, err=True)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, err=True)
```
===== 52 =====
```
     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=None)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=None)

```
===== 53 =====
```
     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            click.echo(spec, file=sys.stdout)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            click.echo(spec, file=sys.stdout)
```
===== 54 =====
```
     # output to local file
     if output_path:
         with open(output_path, 'w') as f:
-            click.echo(spec, file=f)+            json.dump(spec, f)
```
```
@click.command('spec', short_help='Show the OpenAPI spec.')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'yaml', 'yml']),
    help='The format of the spec, defaults to SPEC_FORMAT config.',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='The file path to the spec file, defaults to LOCAL_SPEC_PATH config.',
)
@click.option(
    '--indent',
    '-i',
    type=int,
    help='The indentation for JSON spec, defaults to LOCAL_SPEC_JSON_INDENT config.',
)
@click.option(
    '--quiet', '-q', type=bool, is_flag=True, help='A flag to suppress printing output to stdout.'
)
@with_appcontext
def spec_command(format, output, indent, quiet):
    """Output the OpenAPI spec to stdout or a file.

    Check out the docs for the detailed usage:

    https://apiflask.com/openapi/#the-flask-spec-command
    """
    spec_format = format or current_app.config['SPEC_FORMAT']
    spec = current_app._get_spec(spec_format)
    output_path = output or current_app.config['LOCAL_SPEC_PATH']
    if indent is None:
        indent = current_app.config['LOCAL_SPEC_JSON_INDENT']
    json_indent = None if indent == 0 else indent

    if spec_format == 'json':
        spec = json.dumps(spec, indent=json_indent)

    # output to stdout
    if not quiet:
        click.echo(spec)

    # output to local file
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(spec, f)
```
