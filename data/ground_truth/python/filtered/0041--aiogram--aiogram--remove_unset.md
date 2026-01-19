https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/methods/base.py#L53-L66
```
🈚️

Timeout

@icontract.ensure(lambda OLD: True)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8]
===== 0 =====
```
         but UNSET might be passing to a model initialization from `Bot.method_name`,
         so we must take care of it and remove it before fields validation.
         """
-        if not isinstance(values, dict):
+        if "data" not in values:
             return values
         return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}
```
```
    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.

        We use UNSET as a sentinel value for `parse_mode` and replace it to real value later.
        It isn't a problem when it's just default value for a model field,
        but UNSET might be passing to a model initialization from `Bot.method_name`,
        so we must take care of it and remove it before fields validation.
        """
        if "data" not in values:
            return values
        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}
```
===== 1 =====
```
         but UNSET might be passing to a model initialization from `Bot.method_name`,
         so we must take care of it and remove it before fields validation.
         """
-        if not isinstance(values, dict):
+        if not isinstance(None, dict):
             return values
-        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}+        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}
```
```
    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.

        We use UNSET as a sentinel value for `parse_mode` and replace it to real value later.
        It isn't a problem when it's just default value for a model field,
        but UNSET might be passing to a model initialization from `Bot.method_name`,
        so we must take care of it and remove it before fields validation.
        """
        if not isinstance(None, dict):
            return values
        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}

```
===== 2 =====
```
         """
         if not isinstance(values, dict):
             return values
-        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}+        return {k: v for k, v in values.items() if isinstance(v, (str, int))}
```
```
    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.

        We use UNSET as a sentinel value for `parse_mode` and replace it to real value later.
        It isn't a problem when it's just default value for a model field,
        but UNSET might be passing to a model initialization from `Bot.method_name`,
        so we must take care of it and remove it before fields validation.
        """
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if isinstance(v, (str, int))}
```
===== 3 =====
```
         """
         if not isinstance(values, dict):
             return values
-        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}+        return {k: v for k, v in values.items() if isinstance(v, UNSET_TYPE)}
```
```
    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.

        We use UNSET as a sentinel value for `parse_mode` and replace it to real value later.
        It isn't a problem when it's just default value for a model field,
        but UNSET might be passing to a model initialization from `Bot.method_name`,
        so we must take care of it and remove it before fields validation.
        """
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if isinstance(v, UNSET_TYPE)}
```
===== 4 =====
```
         """
         if not isinstance(values, dict):
             return values
-        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}+        return {k: v for k, v in values.items() if isinstance(v, UNSET_TYPE)}
```
```
    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.

        We use UNSET as a sentinel value for `parse_mode` and replace it to real value later.
        It isn't a problem when it's just default value for a model field,
        but UNSET might be passing to a model initialization from `Bot.method_name`,
        so we must take care of it and remove it before fields validation.
        """
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if isinstance(v, UNSET_TYPE)}

```
===== 5 =====
```
         """
         if not isinstance(values, dict):
             return values
-        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}+        return {k: v for k, v in values.items() if k in values and v is not UNSET_TYPE}
```
```
    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.

        We use UNSET as a sentinel value for `parse_mode` and replace it to real value later.
        It isn't a problem when it's just default value for a model field,
        but UNSET might be passing to a model initialization from `Bot.method_name`,
        so we must take care of it and remove it before fields validation.
        """
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if k in values and v is not UNSET_TYPE}
```
===== 6 =====
```
         """
         if not isinstance(values, dict):
             return values
-        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}+        return {k: v for k, v in values.items() if k not in values or v is not None}
```
```
    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.

        We use UNSET as a sentinel value for `parse_mode` and replace it to real value later.
        It isn't a problem when it's just default value for a model field,
        but UNSET might be passing to a model initialization from `Bot.method_name`,
        so we must take care of it and remove it before fields validation.
        """
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if k not in values or v is not None}
```
===== 7 =====
```
         """
         if not isinstance(values, dict):
             return values
-        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}+        return {k: v for k, v in values.items() if not isinstance(None, UNSET_TYPE)}
```
```
    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.

        We use UNSET as a sentinel value for `parse_mode` and replace it to real value later.
        It isn't a problem when it's just default value for a model field,
        but UNSET might be passing to a model initialization from `Bot.method_name`,
        so we must take care of it and remove it before fields validation.
        """
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if not isinstance(None, UNSET_TYPE)}

```
===== 8 =====
```
         """
         if not isinstance(values, dict):
             return values
-        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}+        return {k: v for k, v in values.items() if v is not UNSET_TYPE}
```
```
    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove UNSET before fields validation.

        We use UNSET as a sentinel value for `parse_mode` and replace it to real value later.
        It isn't a problem when it's just default value for a model field,
        but UNSET might be passing to a model initialization from `Bot.method_name`,
        so we must take care of it and remove it before fields validation.
        """
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if v is not UNSET_TYPE}
```
