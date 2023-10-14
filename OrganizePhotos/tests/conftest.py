import os
from typing import Union

import pytest


@pytest.fixture
def temp_dir(tmp_path):
    yield tmp_path


def given_folder_contains_files(dir_path, filenames: Union[list | str]) -> None:
    if not isinstance(filenames, list):
        filenames = [filenames]
    for filename in filenames:
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "w") as f:
            f.write("Sample file content")
    assert sorted(os.listdir(dir_path)) == sorted(
        filenames
    ), "ERROR: INCORRECTLY PREPARED DATA!"


def create_directory_with_files(temp_dir, dir_path, filenames: Union[list | str]) -> None:
    path = os.path.join(temp_dir, dir_path)
    os.mkdir(path)
    given_folder_contains_files(path, filenames)
