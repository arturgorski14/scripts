import os
import tempfile
from typing import Union

import pytest


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


def given_folder_contains_files(dir_path, filenames: Union[list | str]):
    if not isinstance(filenames, list):
        filenames = [filenames]
    for filename in filenames:
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "w") as f:
            f.write("Sample file content")
    assert sorted(os.listdir(dir_path)) == sorted(filenames), "ERROR: INCORRECTLY PREPARED DATA!"
