

def testsuite_run(lang: str, **kwargs):
    from src.runner.python import python_testsuite_run
    from src.runner.java import java_testsuite_run

    if lang == "python":
        return python_testsuite_run(**kwargs)
    elif lang == "java":
        return java_testsuite_run(**kwargs)
    else:
        raise NotImplementedError()
