https://github.com/pallets-eco/flask-wtf/blob/f7259e91dab7efac8b33c9f86cb86f16f90207a1/./src/flask_wtf/form.py#L88-L119
```
@icontract.snapshot(
    lambda _ARGS: _ARGS[1:], name="fields"
)
@icontract.ensure(
    lambda self, result, OLD: result == Markup(
        "\n".join(
            str(field_obj)
            for f in (OLD.fields or self)
            for field_obj in [
                getattr(self, f, None) if isinstance(f, str) else f
            ]
            if field_obj is not None
            and hasattr(field_obj, "widget")
            and isinstance(field_obj.widget, HiddenInput)
        )
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
===== 0 =====
```
         """
 
         def hidden_fields(fields):
-            for f in fields:
+            for f in self:  # Iterates over the form itself instead of the fields
                 if isinstance(f, str):
                     f = getattr(self, f, None)
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in self:  # Iterates over the form itself instead of the fields
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
===== 1 =====
```
                 if isinstance(f, str):
                     f = getattr(self, f, None)
 
-                if f is None or not isinstance(f.widget, HiddenInput):
+                if f is None and not isinstance(f.widget, HiddenInput):
                     continue
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None and not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))

```
===== 2 =====
```
                 if isinstance(f, str):
                     f = getattr(self, f, None)
 
-                if f is None or not isinstance(f.widget, HiddenInput):
+                if f is None or isinstance(f.widget, HiddenInput) and f.name != 'csrf_token':
                     continue
 
                 yield f
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or isinstance(f.widget, HiddenInput) and f.name != 'csrf_token':
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
===== 3 =====
```
                 if isinstance(f, str):
                     f = getattr(self, f, None)
 
-                if f is None or not isinstance(f.widget, HiddenInput):
+                if f is None or isinstance(f.widget, HiddenInput):
                     continue
 
                 yield f
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
===== 4 =====
```
                 if isinstance(f, str):
                     f = getattr(self, f, None)
 
-                if f is None or not isinstance(f.widget, HiddenInput):
+                if f is None or isinstance(f.widget, HiddenInput):
                     continue
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))

```
===== 5 =====
```
                 if isinstance(f, str):
                     f = getattr(self, f, None)
 
-                if f is None or not isinstance(f.widget, HiddenInput):
+                if f is None or not hasattr(f, 'widget'):
                     continue
 
                 yield f
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not hasattr(f, 'widget'):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
===== 6 =====
```
                 if isinstance(f, str):
                     f = getattr(self, f, None)
 
-                if f is None or not isinstance(f.widget, HiddenInput):
+                if f is None or not isinstance(None, HiddenInput):
                     continue
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(None, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))

```
===== 7 =====
```
                 if isinstance(f, str):
                     f = getattr(self, f, None)
 
-                if f is None or not isinstance(f.widget, HiddenInput):
+                if f is None or not isinstance(f, HiddenInput):
                     continue
 
                 yield f
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
===== 8 =====
```
                 if isinstance(f, str):
                     f = getattr(self, f, None)
 
-                if f is None or not isinstance(f.widget, HiddenInput):
+                if f is not None and isinstance(f.widget, HiddenInput):
                     continue
 
                 yield f
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is not None and isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
===== 9 =====
```
                 if isinstance(f, str):
                     f = getattr(self, f, None)
 
-                if f is None or not isinstance(f.widget, HiddenInput):
+                if f is not None or not isinstance(f.widget, HiddenInput):
                     continue
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is not None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))

```
===== 10 =====
```
                     f = getattr(self, f, None)
 
                 if f is None or not isinstance(f.widget, HiddenInput):
-                    continue
+                    break
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    break

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))

```
===== 11 =====
```
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(None) for f in hidden_fields(fields or self)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(None) for f in hidden_fields(fields or self)))

```
===== 12 =====
```
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields and self)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields and self)))

```
===== 13 =====
```
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields or [])))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or [])))
```
===== 14 =====
```
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields) if f is not None))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields) if f is not None))
```
===== 15 =====
```
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields) if isinstance(f, str)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields) if isinstance(f, str)))
```
===== 16 =====
```
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(fields)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields)))
```
===== 17 =====
```
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup("\n".join(str(f) for f in hidden_fields(self)))
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(self)))
```
===== 18 =====
```
 
                 yield f
 
-        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))+        return Markup(None)
```
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup(None)

```
