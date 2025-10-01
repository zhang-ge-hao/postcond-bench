# Original `pyproject.toml`

```
{original_config}
```

# Guideline

I would like to reproduce a Python project with Poetry. Above is the original `pyproject.toml` file. 

I am in the Docker container environment. The pyenv is installed, maintaining Python versions from 3.6 to 3.11. The Poetry is also installed.

Please provide the command that needs to be run to set the environment, so that this repository can:

1. Install this project by Poetry, i.e., `poetry install` should be runnable.
2. Run unit tests with pytest, i.e., `poetry run pytest` should be runnable.
3. Gather test coverage report with pytest-cov.
4. Get Jsonl format report log with pytest-reportlog.
5. Make the environment support icontract.

If some requirements are not installed for now, you should install them in the commands you responded with.

Note that:

1. Your response should only include the commands you would like to run.
2. Your response should NOT include the commands to actually run `poetry install` or `pytest`, but only the commands to set up the environment, i.e., modify the `pyproject.toml`. For example, `poetry add` or directly modifying the file. The `poetry install` and `pytest` code would be run by other modules and provide feedback to you.
3. If you want to set some environment variables, you should still modify the `pyproject.toml` to use pytest-env.
4. You should NOT create/modify any other files except `pyproject.toml`.
