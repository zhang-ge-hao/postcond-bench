https://github.com/dbcli/litecli/blob/c072661298bc52b10c11e6571cc741a6d41360a7/./litecli/main.py#L671-L722
```
@icontract.snapshot(lambda self: self.prompt_app, name="old_prompt_app")
@icontract.snapshot(lambda self: self.explicit_pager, name="old_explicit_pager")
@icontract.snapshot(lambda self: list(self.query_history), name="old_query_history")
@icontract.snapshot(lambda self: self.logfile, name="old_logfile")
@icontract.snapshot(lambda self: self.formatter, name="old_formatter")
@icontract.snapshot(lambda self: self.sqlexecute, name="old_sqlexecute")
@icontract.ensure(lambda result: result is None)
@icontract.ensure(lambda OLD, self: self.prompt_app is OLD.old_prompt_app)
@icontract.ensure(lambda OLD, self: self.explicit_pager == OLD.old_explicit_pager)
@icontract.ensure(lambda OLD, self: self.query_history == OLD.old_query_history)
@icontract.ensure(lambda OLD, self: self.logfile is OLD.old_logfile)
@icontract.ensure(lambda OLD, self: self.formatter is OLD.old_formatter)
@icontract.ensure(lambda OLD, self: self.sqlexecute is OLD.old_sqlexecute)
```
```
No direct verification.
```
passed
```
@icontract.snapshot(lambda output: list(output), name="old_output")
@icontract.snapshot(lambda self, output, status: (
    setattr(self, "_log_calls", []),
    setattr(self, "_orig_log_output", self.log_output),
    setattr(self, "log_output", (lambda orig, _self=self: (lambda s: (_self._log_calls.append(s), orig(s))[1]))(self.log_output)),
    setattr(click, "_secho_calls", []),
    setattr(click, "_orig_secho", click.secho),
    setattr(click, "secho", (lambda orig: (lambda s, **k: (click._secho_calls.append(s), orig(s, **k))[1]))(click.secho)),
    setattr(click, "_echo_via_pager_calls", []),
    setattr(click, "_orig_echo_via_pager", click.echo_via_pager),
    setattr(click, "echo_via_pager", (lambda orig: (lambda s, **k: (click._echo_via_pager_calls.append(s), orig(s, **k))[1]))(click.echo_via_pager)),
    True
)[-1], name="spies")
@icontract.ensure(lambda OLD, self, output, status: (not OLD.old_output) or (hasattr(self, "_log_calls") and self._log_calls == OLD.old_output))
@icontract.ensure(lambda OLD, self, output, status: (not OLD.old_output) or ((hasattr(click, "_echo_via_pager_calls") and click._echo_via_pager_calls == ["\n".join(OLD.old_output)]) or (hasattr(click, "_secho_calls") and click._secho_calls == OLD.old_output)))
```
===== 23 =====
failed
```
                     click.echo_via_pager("\n".join(buf))
                 else:
                     for line in buf:
-                        click.secho(line)
+                        print(line)  # Using print instead of click.secho will not apply any styling or color.
 
         if status:
             self.log_output(status)
```
```
    def output(self, output, status=None):
        """Output text to stdout or a pager command.

        The status text is not outputted to pager or files.

        The message will be logged in the audit log, if enabled. The
        message will be written to the tee file, if enabled. The
        message will be written to the output file, if enabled.

        """
        if output:
            size = self.prompt_app.output.get_size()

            margin = self.get_output_margin(status)

            fits = True
            buf = []
            output_via_pager = self.explicit_pager and special.is_pager_enabled()
            for i, line in enumerate(output, 1):
                self.log_output(line)
                special.write_tee(line)
                special.write_once(line)
                special.write_pipe_once(line)

                if fits or output_via_pager:
                    # buffering
                    buf.append(line)
                    if len(line) > size.columns or i > (size.rows - margin):
                        fits = False
                        if not self.explicit_pager and special.is_pager_enabled():
                            # doesn't fit, use pager
                            output_via_pager = True

                        if not output_via_pager:
                            # doesn't fit, flush buffer
                            for line in buf:
                                click.secho(line)
                            buf = []
                else:
                    click.secho(line)

            if buf:
                if output_via_pager:
                    # sadly click.echo_via_pager doesn't accept generators
                    click.echo_via_pager("\n".join(buf))
                else:
                    for line in buf:
                        print(line)  # Using print instead of click.secho will not apply any styling or color.

        if status:
            self.log_output(status)
            click.secho(status)
```
