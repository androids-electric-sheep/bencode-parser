import pathlib

import pytest


@pytest.fixture(scope="session")
def data_directory() -> pathlib.Path:
    data_dir = pathlib.Path.cwd() / "data"
    return data_dir
