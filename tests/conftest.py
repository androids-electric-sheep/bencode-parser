import pathlib

import pytest


@pytest.fixture(scope="session")
def data_directory() -> pathlib.Path:
    data_dir = pathlib.Path(__file__).absolute().parent / "data"
    return data_dir
