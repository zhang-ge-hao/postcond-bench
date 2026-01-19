https://github.com/SolaceLabs/solace-agent-mesh/blob/6564748e81c0625394b55124c4d80e4af2f6042b/./cli/utils.py#L30-L61
```
🈚️

No icontract
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
===== 0 =====
```
     Ask a question if the key is not in options or its value is None.
     Updates the options dictionary with the answer and returns the answer.
     """
-    if key not in options or options[key] is None:
+    if key in options and options[key] is not None:
         if none_interactive:
             options[key] = default
         elif is_bool:
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key in options and options[key] is not None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)
```
===== 1 =====
```
     Ask a question if the key is not in options or its value is None.
     Updates the options dictionary with the answer and returns the answer.
     """
-    if key not in options or options[key] is None:
+    if key in options or options[key] is None:
         if none_interactive:
             options[key] = default
         elif is_bool:
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)
```
===== 2 =====
```
     Ask a question if the key is not in options or its value is None.
     Updates the options dictionary with the answer and returns the answer.
     """
-    if key not in options or options[key] is None:
+    if key in options or options[key] is None:
         if none_interactive:
             options[key] = default
         elif is_bool:
@@ -29,4 +29,4 @@             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 3 =====
```
     Ask a question if the key is not in options or its value is None.
     Updates the options dictionary with the answer and returns the answer.
     """
-    if key not in options or options[key] is None:
+    if key not in options and options[key] is None:
         if none_interactive:
             options[key] = default
         elif is_bool:
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options and options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)
```
===== 4 =====
```
     Ask a question if the key is not in options or its value is None.
     Updates the options dictionary with the answer and returns the answer.
     """
-    if key not in options or options[key] is None:
+    if key not in options and options[key] is None:
         if none_interactive:
             options[key] = default
         elif is_bool:
@@ -29,4 +29,4 @@             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options and options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 5 =====
```
     Ask a question if the key is not in options or its value is None.
     Updates the options dictionary with the answer and returns the answer.
     """
-    if key not in options or options[key] is None:
+    if key not in options or options.get(key) is not None:
         if none_interactive:
             options[key] = default
         elif is_bool:
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options.get(key) is not None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)
```
===== 6 =====
```
     Ask a question if the key is not in options or its value is None.
     Updates the options dictionary with the answer and returns the answer.
     """
-    if key not in options or options[key] is None:
+    if key not in options or options[key] is not None:
         if none_interactive:
             options[key] = default
         elif is_bool:
@@ -29,4 +29,4 @@             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is not None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 7 =====
```
     """
     if key not in options or options[key] is None:
         if none_interactive:
-            options[key] = default
+            options[key] = None
         elif is_bool:
             options[key] = ask_yes_no_question(
                 question, default=default if isinstance(default, bool) else False
@@ -29,4 +29,4 @@             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = None
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 8 =====
```
             options[key] = default
         elif is_bool:
             options[key] = ask_yes_no_question(
-                question, default=default if isinstance(default, bool) else False
+                default=default if isinstance(default, bool) else False
             )
         elif choices:
             choice_type = click.Choice(choices)
@@ -29,4 +29,4 @@             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 9 =====
```
             options[key] = default
         elif is_bool:
             options[key] = ask_yes_no_question(
-                question, default=default if isinstance(default, bool) else False
+                question, default=default if isinstance(bool) else False
             )
         elif choices:
             choice_type = click.Choice(choices)
@@ -29,4 +29,4 @@             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 10 =====
```
             options[key] = default
         elif is_bool:
             options[key] = ask_yes_no_question(
-                question, default=default if isinstance(default, bool) else False
+                question, default=default if isinstance(default, ) else False
             )
         elif choices:
             choice_type = click.Choice(choices)
@@ -29,4 +29,4 @@             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, ) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 11 =====
```
             options[key] = default
         elif is_bool:
             options[key] = ask_yes_no_question(
-                question, default=default if isinstance(default, bool) else False
+                question, default=default if isinstance(default, None) else False
             )
         elif choices:
             choice_type = click.Choice(choices)
@@ -29,4 +29,4 @@             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, None) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 12 =====
```
                 question, default=default if isinstance(default, bool) else False
             )
         elif choices:
-            choice_type = click.Choice(choices)
+            choice_type = click.Choice(None)
             options[key] = ask_question(
                 question, default=default, type=choice_type, show_choices=True
             )
@@ -29,4 +29,4 @@             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(None)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 13 =====
```
                 question, default=default if isinstance(default, bool) else False
             )
         elif choices:
-            choice_type = click.Choice(choices)
+            choice_type = click.Choice(choices, help="Choose an option")
             options[key] = ask_question(
                 question, default=default, type=choice_type, show_choices=True
             )
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices, help="Choose an option")
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)
```
===== 14 =====
```
                 question, default=default if isinstance(default, bool) else False
             )
         elif choices:
-            choice_type = click.Choice(choices)
+            choice_type = click.Choice(choices, multiple=True)
             options[key] = ask_question(
                 question, default=default, type=choice_type, show_choices=True
             )
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices, multiple=True)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)
```
===== 15 =====
```
                 question, default=default if isinstance(default, bool) else False
             )
         elif choices:
-            choice_type = click.Choice(choices)
+            choice_type = click.Choice(choices, type=int)
             options[key] = ask_question(
                 question, default=default, type=choice_type, show_choices=True
             )
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices, type=int)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)
```
===== 16 =====
```
                 question, default=default if isinstance(default, bool) else False
             )
         elif choices:
-            choice_type = click.Choice(choices)
+            choice_type = click.Choice(choices, type=str)
             options[key] = ask_question(
                 question, default=default, type=choice_type, show_choices=True
             )
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices, type=str)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)
```
===== 17 =====
```
         elif choices:
             choice_type = click.Choice(choices)
             options[key] = ask_question(
-                question, default=default, type=choice_type, show_choices=True
+                None, default=default, type=choice_type, show_choices=True
             )
         else:
             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                None, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 18 =====
```
                 question, default=default, type=choice_type, show_choices=True
             )
         else:
-            options[key] = ask_question(
-                question, default=default, hide_input=hide_input, type=type
-            )
-    return options.get(key)+            options[key] = None
+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = None
    return options.get(key)

```
===== 19 =====
```
             )
         else:
             options[key] = ask_question(
-                question, default=default, hide_input=hide_input, type=type
+                default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(key)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                default=default, hide_input=hide_input, type=type
            )
    return options.get(key)

```
===== 20 =====
```
             options[key] = ask_question(
                 question, default=default, hide_input=hide_input, type=type
             )
-    return options.get(key)+    return options.get(None)
```
```
def ask_if_not_provided(
    options: dict,
    key: str,
    question: str,
    default=None,
    none_interactive: bool = False,
    choices: list | None = None,
    hide_input: bool = False,
    is_bool: bool = False,
    type=None,
):
    """
    Ask a question if the key is not in options or its value is None.
    Updates the options dictionary with the answer and returns the answer.
    """
    if key not in options or options[key] is None:
        if none_interactive:
            options[key] = default
        elif is_bool:
            options[key] = ask_yes_no_question(
                question, default=default if isinstance(default, bool) else False
            )
        elif choices:
            choice_type = click.Choice(choices)
            options[key] = ask_question(
                question, default=default, type=choice_type, show_choices=True
            )
        else:
            options[key] = ask_question(
                question, default=default, hide_input=hide_input, type=type
            )
    return options.get(None)

```
