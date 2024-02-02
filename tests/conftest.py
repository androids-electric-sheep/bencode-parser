import pathlib

import pytest


@pytest.fixture(scope="session")
def data_directory() -> pathlib.Path:
    data_dir = pathlib.Path(__file__).absolute().parent / "data"
    return data_dir


@pytest.fixture(scope="session")
def torrent_file(data_directory) -> pathlib.Path:
    target_filename = data_directory / "bbb_sunflower_1080p_60fps_normal.mp4.torrent"
    if not target_filename.is_file():
        raise FileNotFoundError(target_filename)
    return target_filename
