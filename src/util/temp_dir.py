import contextlib
import tempfile
import os


@contextlib.contextmanager
def change_dir(path):
    prev = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


@contextlib.contextmanager
def create_tempdir():
    with tempfile.TemporaryDirectory(prefix="sb_tmp_") as dirname:
        with change_dir(dirname):
            yield dirname

