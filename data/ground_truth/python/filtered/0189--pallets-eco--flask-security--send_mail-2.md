https://github.com/pallets-eco/flask-security/blob/06f37fa06ebbb0b9e87cd6819eb44d3aea050f60/./flask_security/utils.py#L864-L901
```
🈚️

Cannot validate send_mail
no mock util can use
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7]
===== 0 =====
```
     body = None
     html = None
     template_path = f"security/email/{template}"
-    if config_value("EMAIL_PLAINTEXT"):
+    if config_value("EMAIL_HTML") and not config_value("EMAIL_PLAINTEXT"):
         body = _security.render_template(f"{template_path}.txt", **context)
     if config_value("EMAIL_HTML"):
         html = _security.render_template(f"{template_path}.html", **context)
```
```
def send_mail(subject, recipient, template, **context):
    """Send an email.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with

    This formats the email and passes it off to :class:`.MailUtil` to actually send the
    message.
    """

    context.setdefault("security", _security)
    context.update(_security._run_ctx_processor("mail"))

    body = None
    html = None
    template_path = f"security/email/{template}"
    if config_value("EMAIL_HTML") and not config_value("EMAIL_PLAINTEXT"):
        body = _security.render_template(f"{template_path}.txt", **context)
    if config_value("EMAIL_HTML"):
        html = _security.render_template(f"{template_path}.html", **context)

    subject = localize_callback(subject)

    sender = config_value("EMAIL_SENDER")
    if isinstance(sender, LocalProxy):
        sender = sender._get_current_object()

    _security.mail_util.send_mail(
        template,
        subject,
        recipient,
        sender,
        body,
        html,
        **context,
    )
```
===== 1 =====
```
     body = None
     html = None
     template_path = f"security/email/{template}"
-    if config_value("EMAIL_PLAINTEXT"):
+    if config_value("EMAIL_PLAINTEXT") == "true":
         body = _security.render_template(f"{template_path}.txt", **context)
     if config_value("EMAIL_HTML"):
         html = _security.render_template(f"{template_path}.html", **context)
```
```
def send_mail(subject, recipient, template, **context):
    """Send an email.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with

    This formats the email and passes it off to :class:`.MailUtil` to actually send the
    message.
    """

    context.setdefault("security", _security)
    context.update(_security._run_ctx_processor("mail"))

    body = None
    html = None
    template_path = f"security/email/{template}"
    if config_value("EMAIL_PLAINTEXT") == "true":
        body = _security.render_template(f"{template_path}.txt", **context)
    if config_value("EMAIL_HTML"):
        html = _security.render_template(f"{template_path}.html", **context)

    subject = localize_callback(subject)

    sender = config_value("EMAIL_SENDER")
    if isinstance(sender, LocalProxy):
        sender = sender._get_current_object()

    _security.mail_util.send_mail(
        template,
        subject,
        recipient,
        sender,
        body,
        html,
        **context,
    )
```
===== 2 =====
```
     body = None
     html = None
     template_path = f"security/email/{template}"
-    if config_value("EMAIL_PLAINTEXT"):
+    if config_value("EMAIL_PLAINTEXT") == False:
         body = _security.render_template(f"{template_path}.txt", **context)
     if config_value("EMAIL_HTML"):
         html = _security.render_template(f"{template_path}.html", **context)
```
```
def send_mail(subject, recipient, template, **context):
    """Send an email.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with

    This formats the email and passes it off to :class:`.MailUtil` to actually send the
    message.
    """

    context.setdefault("security", _security)
    context.update(_security._run_ctx_processor("mail"))

    body = None
    html = None
    template_path = f"security/email/{template}"
    if config_value("EMAIL_PLAINTEXT") == False:
        body = _security.render_template(f"{template_path}.txt", **context)
    if config_value("EMAIL_HTML"):
        html = _security.render_template(f"{template_path}.html", **context)

    subject = localize_callback(subject)

    sender = config_value("EMAIL_SENDER")
    if isinstance(sender, LocalProxy):
        sender = sender._get_current_object()

    _security.mail_util.send_mail(
        template,
        subject,
        recipient,
        sender,
        body,
        html,
        **context,
    )
```
===== 3 =====
```
     body = None
     html = None
     template_path = f"security/email/{template}"
-    if config_value("EMAIL_PLAINTEXT"):
+    if config_value("EMAIL_PLAINTEXT") is None:
         body = _security.render_template(f"{template_path}.txt", **context)
     if config_value("EMAIL_HTML"):
         html = _security.render_template(f"{template_path}.html", **context)
```
```
def send_mail(subject, recipient, template, **context):
    """Send an email.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with

    This formats the email and passes it off to :class:`.MailUtil` to actually send the
    message.
    """

    context.setdefault("security", _security)
    context.update(_security._run_ctx_processor("mail"))

    body = None
    html = None
    template_path = f"security/email/{template}"
    if config_value("EMAIL_PLAINTEXT") is None:
        body = _security.render_template(f"{template_path}.txt", **context)
    if config_value("EMAIL_HTML"):
        html = _security.render_template(f"{template_path}.html", **context)

    subject = localize_callback(subject)

    sender = config_value("EMAIL_SENDER")
    if isinstance(sender, LocalProxy):
        sender = sender._get_current_object()

    _security.mail_util.send_mail(
        template,
        subject,
        recipient,
        sender,
        body,
        html,
        **context,
    )
```
===== 4 =====
```
     body = None
     html = None
     template_path = f"security/email/{template}"
-    if config_value("EMAIL_PLAINTEXT"):
+    if not config_value("EMAIL_PLAINTEXT") and config_value("EMAIL_HTML"):
         body = _security.render_template(f"{template_path}.txt", **context)
     if config_value("EMAIL_HTML"):
         html = _security.render_template(f"{template_path}.html", **context)
```
```
def send_mail(subject, recipient, template, **context):
    """Send an email.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with

    This formats the email and passes it off to :class:`.MailUtil` to actually send the
    message.
    """

    context.setdefault("security", _security)
    context.update(_security._run_ctx_processor("mail"))

    body = None
    html = None
    template_path = f"security/email/{template}"
    if not config_value("EMAIL_PLAINTEXT") and config_value("EMAIL_HTML"):
        body = _security.render_template(f"{template_path}.txt", **context)
    if config_value("EMAIL_HTML"):
        html = _security.render_template(f"{template_path}.html", **context)

    subject = localize_callback(subject)

    sender = config_value("EMAIL_SENDER")
    if isinstance(sender, LocalProxy):
        sender = sender._get_current_object()

    _security.mail_util.send_mail(
        template,
        subject,
        recipient,
        sender,
        body,
        html,
        **context,
    )
```
===== 5 =====
```
     html = None
     template_path = f"security/email/{template}"
     if config_value("EMAIL_PLAINTEXT"):
-        body = _security.render_template(f"{template_path}.txt", **context)
+        body = None
     if config_value("EMAIL_HTML"):
         html = _security.render_template(f"{template_path}.html", **context)
 
@@ -35,4 +35,4 @@         body,
         html,
         **context,
-    )+    )
```
```
def send_mail(subject, recipient, template, **context):
    """Send an email.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with

    This formats the email and passes it off to :class:`.MailUtil` to actually send the
    message.
    """

    context.setdefault("security", _security)
    context.update(_security._run_ctx_processor("mail"))

    body = None
    html = None
    template_path = f"security/email/{template}"
    if config_value("EMAIL_PLAINTEXT"):
        body = None
    if config_value("EMAIL_HTML"):
        html = _security.render_template(f"{template_path}.html", **context)

    subject = localize_callback(subject)

    sender = config_value("EMAIL_SENDER")
    if isinstance(sender, LocalProxy):
        sender = sender._get_current_object()

    _security.mail_util.send_mail(
        template,
        subject,
        recipient,
        sender,
        body,
        html,
        **context,
    )

```
===== 6 =====
```
     html = None
     template_path = f"security/email/{template}"
     if config_value("EMAIL_PLAINTEXT"):
-        body = _security.render_template(f"{template_path}.txt", **context)
+        body = _security.render_template(f"{template_path}.txt", **{**context, "user": None})  # Overwriting user context
     if config_value("EMAIL_HTML"):
         html = _security.render_template(f"{template_path}.html", **context)
```
```
def send_mail(subject, recipient, template, **context):
    """Send an email.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with

    This formats the email and passes it off to :class:`.MailUtil` to actually send the
    message.
    """

    context.setdefault("security", _security)
    context.update(_security._run_ctx_processor("mail"))

    body = None
    html = None
    template_path = f"security/email/{template}"
    if config_value("EMAIL_PLAINTEXT"):
        body = _security.render_template(f"{template_path}.txt", **{**context, "user": None})  # Overwriting user context
    if config_value("EMAIL_HTML"):
        html = _security.render_template(f"{template_path}.html", **context)

    subject = localize_callback(subject)

    sender = config_value("EMAIL_SENDER")
    if isinstance(sender, LocalProxy):
        sender = sender._get_current_object()

    _security.mail_util.send_mail(
        template,
        subject,
        recipient,
        sender,
        body,
        html,
        **context,
    )
```
===== 7 =====
```
         subject,
         recipient,
         sender,
-        body,
+        None,
         html,
         **context,
-    )+    )
```
```
def send_mail(subject, recipient, template, **context):
    """Send an email.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with

    This formats the email and passes it off to :class:`.MailUtil` to actually send the
    message.
    """

    context.setdefault("security", _security)
    context.update(_security._run_ctx_processor("mail"))

    body = None
    html = None
    template_path = f"security/email/{template}"
    if config_value("EMAIL_PLAINTEXT"):
        body = _security.render_template(f"{template_path}.txt", **context)
    if config_value("EMAIL_HTML"):
        html = _security.render_template(f"{template_path}.html", **context)

    subject = localize_callback(subject)

    sender = config_value("EMAIL_SENDER")
    if isinstance(sender, LocalProxy):
        sender = sender._get_current_object()

    _security.mail_util.send_mail(
        template,
        subject,
        recipient,
        sender,
        None,
        html,
        **context,
    )

```
