https://github.com/pallets-eco/flask-security/blob/06f37fa06ebbb0b9e87cd6819eb44d3aea050f60/./flask_security/registerable.py#L36-L80
```
🈚️

half of the method is about sending email, which is not validatable.

mock util needed

@icontract.snapshot(
    lambda registration_form: registration_form.to_dict(only_user=True),
    name="orig_user_data",
)
@icontract.ensure(
    lambda result: result is not None,
    "register_user must return a user object.",
)
@icontract.ensure(
    lambda result, OLD:
        # 所有非 password 字段在 user 上要保持一致
        all(
            field == "password" or getattr(result, field) == value
            for field, value in OLD.orig_user_data.items()
        ),
    "All non-password user fields must match the registration form.",
)
@icontract.ensure(
    lambda result, OLD:
        # 如果表单里提供了密码，则返回的 user.password 不能等于明文
        (
            not OLD.orig_user_data.get("password")
            or (
                getattr(result, "password", None) is not None
                and getattr(result, "password") != OLD.orig_user_data.get("password")
            )
        ),
    "When a password is supplied, it must not be stored in plain text.",
)
@icontract.ensure(
    lambda result, OLD:
        # 如果表单里没有提供密码，则 user.password 应该也是“空”的
        (
            OLD.orig_user_data.get("password")
            or not getattr(result, "password", None)
        ),
    "When no password is supplied, the stored password must be empty/falsy.",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
===== 0 =====
```
 
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
-    if user_model_kwargs["password"]:
+    if len(user_model_kwargs["password"]) < 8:  # Introduces a length check that may skip valid passwords
         user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
     user = _datastore.create_user(**user_model_kwargs)
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if len(user_model_kwargs["password"]) < 8:  # Introduces a length check that may skip valid passwords
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 1 =====
```
 
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
-    if user_model_kwargs["password"]:
+    if not user_model_kwargs["password"]:  # Negates the condition, leading to incorrect behavior
         user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
     user = _datastore.create_user(**user_model_kwargs)
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if not user_model_kwargs["password"]:  # Negates the condition, leading to incorrect behavior
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 2 =====
```
 
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
-    if user_model_kwargs["password"]:
+    if user_model_kwargs.get("password") is None:  # Incorrectly checks for None instead of presence
         user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
     user = _datastore.create_user(**user_model_kwargs)
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs.get("password") is None:  # Incorrectly checks for None instead of presence
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 3 =====
```
 
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
-    if user_model_kwargs["password"]:
+    if user_model_kwargs["password"] == "":  # Incorrectly checks for an empty string instead of presence
         user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
     user = _datastore.create_user(**user_model_kwargs)
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"] == "":  # Incorrectly checks for an empty string instead of presence
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 4 =====
```
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
     if user_model_kwargs["password"]:
-        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
+        user_model_kwargs["password"] = None
     user = _datastore.create_user(**user_model_kwargs)
 
     # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
@@ -42,4 +42,4 @@             confirmation_token=token,
         )
 
-    return user+    return user
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = None
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user

```
===== 5 =====
```
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
     if user_model_kwargs["password"]:
-        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
+        user_model_kwargs["password"] = None  # Sets password to None, making it unusable
     user = _datastore.create_user(**user_model_kwargs)
 
     # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = None  # Sets password to None, making it unusable
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 6 =====
```
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
     if user_model_kwargs["password"]:
-        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
+        user_model_kwargs["password"] = hash_password("")  # Sets password to a blank hash
     user = _datastore.create_user(**user_model_kwargs)
 
     # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password("")  # Sets password to a blank hash
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 7 =====
```
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
     if user_model_kwargs["password"]:
-        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
+        user_model_kwargs["password"] = hash_password(None)
     user = _datastore.create_user(**user_model_kwargs)
 
     # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
@@ -42,4 +42,4 @@             confirmation_token=token,
         )
 
-    return user+    return user
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(None)
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user

```
===== 8 =====
```
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
     if user_model_kwargs["password"]:
-        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
+        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"] + "123")  # Incorrectly modifies the password
     user = _datastore.create_user(**user_model_kwargs)
 
     # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"] + "123")  # Incorrectly modifies the password
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 9 =====
```
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
     if user_model_kwargs["password"]:
-        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
+        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"].upper())  # Changes password to uppercase before hashing
     user = _datastore.create_user(**user_model_kwargs)
 
     # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"].upper())  # Changes password to uppercase before hashing
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 10 =====
```
     # passwords are not always required -
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
     if user_model_kwargs["password"]:
-        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
+        user_model_kwargs["password"] = user_model_kwargs["password"]  # No hashing applied
     user = _datastore.create_user(**user_model_kwargs)
 
     # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = user_model_kwargs["password"]  # No hashing applied
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 11 =====
```
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
     if user_model_kwargs["password"]:
         user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
-    user = _datastore.create_user(**user_model_kwargs)
+    user = _datastore.create_user(**user_model_kwargs, active=False)  # User is created but inactive
 
     # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
     if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs, active=False)  # User is created but inactive

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 12 =====
```
     # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
     if user_model_kwargs["password"]:
         user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
-    user = _datastore.create_user(**user_model_kwargs)
+    user = _datastore.create_user(**{**user_model_kwargs, "password": None})  # Password is set to None
 
     # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
     if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**{**user_model_kwargs, "password": None})  # Password is set to None

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 13 =====
```
         _datastore.us_setup_email(user)
 
     confirmation_link, token = None, None
-    if _security.confirmable:
+    if _security.confirmable is None:
         confirmation_link, token = generate_confirmation_link(user)
         do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable is None:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 14 =====
```
 
     confirmation_link, token = None, None
     if _security.confirmable:
-        confirmation_link, token = generate_confirmation_link(user)
+        confirmation_link, token = (None, None)  # No confirmation link generated
         do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))
 
     user_registered.send(
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = (None, None)  # No confirmation link generated
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 15 =====
```
 
     confirmation_link, token = None, None
     if _security.confirmable:
-        confirmation_link, token = generate_confirmation_link(user)
+        confirmation_link, token = generate_confirmation_link(user) if not user.is_active else (None, None)
         do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))
 
     user_registered.send(
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user) if not user.is_active else (None, None)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 16 =====
```
         do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))
 
     user_registered.send(
-        current_app._get_current_object(),
+        None,
         _async_wrapper=current_app.ensure_sync,
         user=user,
         confirm_token=token,
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        None,
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 17 =====
```
         do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))
 
     user_registered.send(
-        current_app._get_current_object(),
+        None,
         _async_wrapper=current_app.ensure_sync,
         user=user,
         confirm_token=token,
@@ -42,4 +42,4 @@             confirmation_token=token,
         )
 
-    return user+    return user
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        None,
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user

```
===== 18 =====
```
         do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))
 
     user_registered.send(
-        current_app._get_current_object(),
         _async_wrapper=current_app.ensure_sync,
         user=user,
         confirm_token=token,
@@ -42,4 +41,4 @@             confirmation_token=token,
         )
 
-    return user+    return user
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user

```
===== 19 =====
```
         do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))
 
     user_registered.send(
-        current_app._get_current_object(),
+        current_app,
         _async_wrapper=current_app.ensure_sync,
         user=user,
         confirm_token=token,
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app,
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 20 =====
```
         do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))
 
     user_registered.send(
-        current_app._get_current_object(),
+        current_app._get_current_object() if False else None,
         _async_wrapper=current_app.ensure_sync,
         user=user,
         confirm_token=token,
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object() if False else None,
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 21 =====
```
         do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))
 
     user_registered.send(
-        current_app._get_current_object(),
+        current_app._get_current_object() if not current_app else current_app,
         _async_wrapper=current_app.ensure_sync,
         user=user,
         confirm_token=token,
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object() if not current_app else current_app,
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 22 =====
```
         current_app._get_current_object(),
         _async_wrapper=current_app.ensure_sync,
         user=user,
-        confirm_token=token,
+        confirm_token=None,
         confirmation_token=token,
         form_data=registration_form.to_dict(only_user=False),
     )
@@ -42,4 +42,4 @@             confirmation_token=token,
         )
 
-    return user+    return user
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=None,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user

```
===== 23 =====
```
         form_data=registration_form.to_dict(only_user=False),
     )
 
-    if cv("SEND_REGISTER_EMAIL"):
+    if cv("SEND_REGISTER_EMAIL") and not user.email:
         send_mail(
             cv("EMAIL_SUBJECT_REGISTER"),
             user.email,
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL") and not user.email:
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 24 =====
```
         form_data=registration_form.to_dict(only_user=False),
     )
 
-    if cv("SEND_REGISTER_EMAIL"):
+    if cv("SEND_REGISTER_EMAIL") and user is None:
         send_mail(
             cv("EMAIL_SUBJECT_REGISTER"),
             user.email,
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL") and user is None:
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 25 =====
```
         form_data=registration_form.to_dict(only_user=False),
     )
 
-    if cv("SEND_REGISTER_EMAIL"):
+    if cv("SEND_REGISTER_EMAIL") and user.email == "test@example.com":
         send_mail(
             cv("EMAIL_SUBJECT_REGISTER"),
             user.email,
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if cv("SEND_REGISTER_EMAIL") and user.email == "test@example.com":
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
===== 26 =====
```
         form_data=registration_form.to_dict(only_user=False),
     )
 
-    if cv("SEND_REGISTER_EMAIL"):
+    if not cv("SEND_REGISTER_EMAIL"):
         send_mail(
             cv("EMAIL_SUBJECT_REGISTER"),
             user.email,
```
```
def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    # passwords are not always required -
    # with UNIFIED_SIGNIN and PASSWORD_REQUIRED=False
    if user_model_kwargs["password"]:
        user_model_kwargs["password"] = hash_password(user_model_kwargs["password"])
    user = _datastore.create_user(**user_model_kwargs)

    # if they didn't give a password - auto-setup email magic links (if UNIFIED SIGNIN)
    if not user_model_kwargs["password"] and cv("UNIFIED_SIGNIN"):
        _datastore.us_setup_email(user)

    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        current_app._get_current_object(),
        _async_wrapper=current_app.ensure_sync,
        user=user,
        confirm_token=token,
        confirmation_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if not cv("SEND_REGISTER_EMAIL"):
        send_mail(
            cv("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
            confirmation_token=token,
        )

    return user
```
