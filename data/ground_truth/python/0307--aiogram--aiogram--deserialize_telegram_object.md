https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/utils/serialization.py#L34-L68
```
@icontract.snapshot(lambda obj: obj, name="orig_obj")
@icontract.snapshot(lambda default: default, name="orig_default")
@icontract.snapshot(lambda include_api_method_name: include_api_method_name, name="orig_include")
@icontract.ensure(lambda result: isinstance(result, DeserializedTelegramObject))
@icontract.ensure(
    lambda result:
    isinstance(result.files, dict)
    and all(isinstance(k, str) for k in result.files.keys())
    and all(isinstance(v, InputFile) for v in result.files.values())
)
@icontract.ensure(lambda result: result.data is not result.files)
@icontract.ensure(lambda result: result.data is not None)
@icontract.ensure(
    lambda OLD, result:
    (not isinstance(OLD.orig_obj, BaseModel))
    or (isinstance(result.data, dict) and not isinstance(result.data, BaseModel))
)
@icontract.ensure(
    lambda OLD, result:
    (not OLD.orig_include or not isinstance(OLD.orig_obj, TelegramMethod))
    or (isinstance(result.data, dict)
        and result.data.get("method") == OLD.orig_obj.__api_method__)
)
@icontract.ensure(
    lambda OLD, result:
    (
        lambda orig_obj, default, include_flag:
            (
                lambda obj_for_prepare, extends:
                    (
                        lambda fake_bot, files:
                            (
                                lambda prepared:
                                    (
                                        (prepared.update(extends) or True)
                                        if isinstance(prepared, dict)
                                        else True
                                    )
                                    and result.data == prepared
                                    and result.files == files
                            )(
                                fake_bot.session.prepare_value(
                                    obj_for_prepare,
                                    bot=fake_bot,
                                    files=files,
                                    _dumps_json=False,
                                )
                            )
                    )(
                        _get_fake_bot(default=default),
                        {},
                    )
            )(
                orig_obj.model_dump(mode="python", warnings=False)
                if isinstance(orig_obj, BaseModel)
                else orig_obj,
                (
                    {"method": orig_obj.__api_method__}
                    if include_flag and isinstance(orig_obj, TelegramMethod)
                    else {}
                ),
            )
    )(
        OLD.orig_obj,
        OLD.orig_default,
        OLD.orig_include,
    )
)
```
```
@icontract.snapshot(lambda obj: obj, name="orig_obj")
@icontract.snapshot(lambda default: default, name="orig_default")
@icontract.snapshot(lambda include_api_method_name: include_api_method_name, name="orig_include")
@icontract.ensure(lambda result: isinstance(result, DeserializedTelegramObject))
@icontract.ensure(lambda result: isinstance(result.files, dict) and all(isinstance(k, str) for k in result.files.keys()) and all(isinstance(v, InputFile) for v in result.files.values()))
@icontract.ensure(lambda result: result.data is not result.files)
@icontract.ensure(lambda result: result.data is not None)
@icontract.ensure(lambda OLD, result: (not isinstance(OLD.orig_obj, BaseModel)) or (isinstance(result.data, dict) and not isinstance(result.data, BaseModel)))
@icontract.ensure(lambda OLD, result: (not OLD.orig_include or not isinstance(OLD.orig_obj, TelegramMethod)) or (isinstance(result.data, dict) and result.data.get("method") == OLD.orig_obj.__api_method__))
```
[7, 8, 9, 10, 20]
===== 7 =====
```
         obj = obj.model_dump(mode="python", warnings=False)
 
     # Fake bot is needed to exclude global defaults from the object.
-    fake_bot = _get_fake_bot(default=default)
+    fake_bot = _get_fake_bot()  # Calling without any arguments, which uses default properties
 
     files: dict[str, InputFile] = {}
     prepared = fake_bot.session.prepare_value(
```
```
def deserialize_telegram_object(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> DeserializedTelegramObject:
    """
    Deserialize Telegram Object to JSON compatible Python object.

    :param obj: The object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized Telegram object.
    """
    extends = {}
    if include_api_method_name and isinstance(obj, TelegramMethod):
        extends["method"] = obj.__api_method__

    if isinstance(obj, BaseModel):
        obj = obj.model_dump(mode="python", warnings=False)

    # Fake bot is needed to exclude global defaults from the object.
    fake_bot = _get_fake_bot()  # Calling without any arguments, which uses default properties

    files: dict[str, InputFile] = {}
    prepared = fake_bot.session.prepare_value(
        obj,
        bot=fake_bot,
        files=files,
        _dumps_json=False,
    )

    if isinstance(prepared, dict):
        prepared.update(extends)
    return DeserializedTelegramObject(data=prepared, files=files)
```
===== 8 =====
```
         obj = obj.model_dump(mode="python", warnings=False)
 
     # Fake bot is needed to exclude global defaults from the object.
-    fake_bot = _get_fake_bot(default=default)
+    fake_bot = _get_fake_bot(default=DefaultBotProperties())  # Creating a new DefaultBotProperties instance instead of using the provided one
 
     files: dict[str, InputFile] = {}
     prepared = fake_bot.session.prepare_value(
```
```
def deserialize_telegram_object(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> DeserializedTelegramObject:
    """
    Deserialize Telegram Object to JSON compatible Python object.

    :param obj: The object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized Telegram object.
    """
    extends = {}
    if include_api_method_name and isinstance(obj, TelegramMethod):
        extends["method"] = obj.__api_method__

    if isinstance(obj, BaseModel):
        obj = obj.model_dump(mode="python", warnings=False)

    # Fake bot is needed to exclude global defaults from the object.
    fake_bot = _get_fake_bot(default=DefaultBotProperties())  # Creating a new DefaultBotProperties instance instead of using the provided one

    files: dict[str, InputFile] = {}
    prepared = fake_bot.session.prepare_value(
        obj,
        bot=fake_bot,
        files=files,
        _dumps_json=False,
    )

    if isinstance(prepared, dict):
        prepared.update(extends)
    return DeserializedTelegramObject(data=prepared, files=files)
```
===== 9 =====
```
         obj = obj.model_dump(mode="python", warnings=False)
 
     # Fake bot is needed to exclude global defaults from the object.
-    fake_bot = _get_fake_bot(default=default)
+    fake_bot = _get_fake_bot(default=None)
 
     files: dict[str, InputFile] = {}
     prepared = fake_bot.session.prepare_value(
@@ -32,4 +32,4 @@ 
     if isinstance(prepared, dict):
         prepared.update(extends)
-    return DeserializedTelegramObject(data=prepared, files=files)+    return DeserializedTelegramObject(data=prepared, files=files)
```
```
def deserialize_telegram_object(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> DeserializedTelegramObject:
    """
    Deserialize Telegram Object to JSON compatible Python object.

    :param obj: The object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized Telegram object.
    """
    extends = {}
    if include_api_method_name and isinstance(obj, TelegramMethod):
        extends["method"] = obj.__api_method__

    if isinstance(obj, BaseModel):
        obj = obj.model_dump(mode="python", warnings=False)

    # Fake bot is needed to exclude global defaults from the object.
    fake_bot = _get_fake_bot(default=None)

    files: dict[str, InputFile] = {}
    prepared = fake_bot.session.prepare_value(
        obj,
        bot=fake_bot,
        files=files,
        _dumps_json=False,
    )

    if isinstance(prepared, dict):
        prepared.update(extends)
    return DeserializedTelegramObject(data=prepared, files=files)

```
===== 10 =====
```
         obj = obj.model_dump(mode="python", warnings=False)
 
     # Fake bot is needed to exclude global defaults from the object.
-    fake_bot = _get_fake_bot(default=default)
+    fake_bot = _get_fake_bot(default=None)  # Using None instead of the provided default
 
     files: dict[str, InputFile] = {}
     prepared = fake_bot.session.prepare_value(
```
```
def deserialize_telegram_object(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> DeserializedTelegramObject:
    """
    Deserialize Telegram Object to JSON compatible Python object.

    :param obj: The object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized Telegram object.
    """
    extends = {}
    if include_api_method_name and isinstance(obj, TelegramMethod):
        extends["method"] = obj.__api_method__

    if isinstance(obj, BaseModel):
        obj = obj.model_dump(mode="python", warnings=False)

    # Fake bot is needed to exclude global defaults from the object.
    fake_bot = _get_fake_bot(default=None)  # Using None instead of the provided default

    files: dict[str, InputFile] = {}
    prepared = fake_bot.session.prepare_value(
        obj,
        bot=fake_bot,
        files=files,
        _dumps_json=False,
    )

    if isinstance(prepared, dict):
        prepared.update(extends)
    return DeserializedTelegramObject(data=prepared, files=files)
```
===== 20 =====
```
     )
 
     if isinstance(prepared, dict):
-        prepared.update(extends)
+        prepared = extends  # This will overwrite prepared with extends
     return DeserializedTelegramObject(data=prepared, files=files)
```
```
def deserialize_telegram_object(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> DeserializedTelegramObject:
    """
    Deserialize Telegram Object to JSON compatible Python object.

    :param obj: The object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized Telegram object.
    """
    extends = {}
    if include_api_method_name and isinstance(obj, TelegramMethod):
        extends["method"] = obj.__api_method__

    if isinstance(obj, BaseModel):
        obj = obj.model_dump(mode="python", warnings=False)

    # Fake bot is needed to exclude global defaults from the object.
    fake_bot = _get_fake_bot(default=default)

    files: dict[str, InputFile] = {}
    prepared = fake_bot.session.prepare_value(
        obj,
        bot=fake_bot,
        files=files,
        _dumps_json=False,
    )

    if isinstance(prepared, dict):
        prepared = extends  # This will overwrite prepared with extends
    return DeserializedTelegramObject(data=prepared, files=files)
```
