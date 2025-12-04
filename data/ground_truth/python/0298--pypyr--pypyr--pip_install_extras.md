https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/venv.py#L212-L238
```
@icontract.snapshot(
    lambda self, pip_args: [
        os.path.expanduser(v)
        for v in (
            shlex.split(pip_args)
            if isinstance(pip_args, str)
            else list(pip_args)
        )
    ],
    name="expected_deps",
)
@icontract.snapshot(
    lambda self, pip_args: [
        self.context.env_exec_cmd,
        "-m",
        "pip",
        "install",
    ]
    + (["-q"] if self.is_quiet else [])
    + [
        os.path.expanduser(v)
        for v in (
            shlex.split(pip_args)
            if isinstance(pip_args, str)
            else list(pip_args)
        )
    ],
    name="expected_cmd",
)
@icontract.ensure(lambda result: result is None)
@icontract.ensure(
    lambda OLD: (
        not hasattr(subprocess.run, "call_count")
        or (
            subprocess.run.call_count == 1
            and len(subprocess.run.call_args[0]) >= 1
            and subprocess.run.call_args[0][0] == OLD.expected_cmd
            and subprocess.run.call_args[1].get("check") is True
        )
    )
)
@icontract.ensure(
    lambda: (
        not hasattr(subprocess.check_output, "call_count")
        or subprocess.check_output.call_count == 0
    )
)
```
```
@icontract.snapshot(lambda self, pip_args: [os.path.expanduser(v) for v in (shlex.split(pip_args) if isinstance(pip_args, str) else list(pip_args))], name="expected_deps")
@icontract.snapshot(lambda self, pip_args: [self.context.env_exec_cmd, '-m', 'pip', 'install'] + (['-q'] if self.is_quiet else []) + [os.path.expanduser(v) for v in (shlex.split(pip_args) if isinstance(pip_args, str) else list(pip_args))], name="expected_cmd")
@icontract.ensure(lambda result: result is None)
@icontract.ensure(lambda OLD: hasattr(subprocess.run, "call_count") and subprocess.run.call_count == 1 and subprocess.run.call_args[0][0] == OLD.expected_cmd and subprocess.run.call_args[1].get('check') is True)
```
[25, 27]
===== 25 =====
```
         cmd.extend(shlexed_deps)
 
         logger.debug("running %s", cmd)
-        subprocess.run(cmd, check=True)
+        subprocess.check_output(cmd)  # This will return the output instead of checking for success, potentially masking errors.
 
         logger.debug("done")
```
```
    def pip_install_extras(self, pip_args: str) -> None:
        """Run python -m pip install {pip_args} in venv.

        You can ONLY call this AFTER post_setup() has run, which in practice
        means you have to have called create().
        """
        logger.debug("installing extra dependencies for path %s",
                     self.context.env_dir)

        cmd = [self.context.env_exec_cmd, '-m', 'pip', 'install']
        if self.is_quiet:
            cmd.append('-q')

        # if input is a list already, no need to shlex split
        shlexed_deps = shlex.split(pip_args) if isinstance(pip_args,
                                                           str) else pip_args

        # each arg could contain a path, thus run expand on all args
        for i, v in enumerate(shlexed_deps):
            shlexed_deps[i] = os.path.expanduser(v)

        cmd.extend(shlexed_deps)

        logger.debug("running %s", cmd)
        subprocess.check_output(cmd)  # This will return the output instead of checking for success, potentially masking errors.

        logger.debug("done")
```
===== 27 =====
```
         cmd.extend(shlexed_deps)
 
         logger.debug("running %s", cmd)
-        subprocess.run(cmd, check=True)
+        subprocess.run(check=True)
 
-        logger.debug("done")+        logger.debug("done")
```
```
    def pip_install_extras(self, pip_args: str) -> None:
        """Run python -m pip install {pip_args} in venv.

        You can ONLY call this AFTER post_setup() has run, which in practice
        means you have to have called create().
        """
        logger.debug("installing extra dependencies for path %s",
                     self.context.env_dir)

        cmd = [self.context.env_exec_cmd, '-m', 'pip', 'install']
        if self.is_quiet:
            cmd.append('-q')

        # if input is a list already, no need to shlex split
        shlexed_deps = shlex.split(pip_args) if isinstance(pip_args,
                                                           str) else pip_args

        # each arg could contain a path, thus run expand on all args
        for i, v in enumerate(shlexed_deps):
            shlexed_deps[i] = os.path.expanduser(v)

        cmd.extend(shlexed_deps)

        logger.debug("running %s", cmd)
        subprocess.run(check=True)

        logger.debug("done")

```
