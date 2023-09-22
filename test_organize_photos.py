import os
import re
import tempfile
from typing import Pattern, Union

import pytest
from organize_photos import (
    GetPhotosFromDirectory,
    MoveFilesToFolders,
)

EXPECTED_FILENAME_PATTERN: Pattern[str] = re.compile(r"^IMG_\d{8}_\d{6}\.jpg$")


# Define a fixture to create a temporary directory for testing
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


@pytest.mark.parametrize("filename", ["IMG_20220410_105512.jpg"])
def test_is_valid_filename_success(filename):
    command = GetPhotosFromDirectory()
    assert (
        command.validate_filename(filename) is True
    ), f"{filename=} doesnt match pattern {EXPECTED_FILENAME_PATTERN}"


@pytest.mark.parametrize(
    "filename",
    [
        "not_matching_filenames.jpg",
        "IM_20220410_105512.jpg",
        "IMM_20220410_105512.jpg",
        "IMMG_20220410_105512.jpg",
        "IMG_202220410_105512.jpg",
        "IMG_2020410_105512.jpg",
        "IMG_20220410_1055512.jpg",
        "IMG_20220410_10512.jpg",
        "IMG_IMG_20220410_105512.jpg",
        "IMG_20220410_105512.jpgg",
        "IIMG_20220410_105512.jpg" "IMG_20220410_105512.jpgg",
        "IMG_20220410_105512.png",
        "IMG_20220410_105512.webp",
        "IMG_20220410_105512.jpeg",
        "IMG_20220410_105512.csv",
    ],
)
def test_is_valid_filename_failure(filename):
    command = GetPhotosFromDirectory()
    assert command.validate_filename(filename) is False


@pytest.mark.parametrize(
    "filenames, expected_result",
    [
        (
            [
                "folder",
                "2022.04.10",
                "not_matching_filename",
                "IM_20220410_105512.jpg",
                "IMM_20220410_105512.jpg",
            ],
            {},
        ),
        (
            [
                "2022.03.05",
                "IMG_20220305_132952.jpg",
                "IMG_20220306_143021.jpg",
                "IMG_20220410_105512.jpg",
            ],
            {
                "2022.03.05": ["IMG_20220305_132952.jpg"],
                "2022.03.06": ["IMG_20220306_143021.jpg"],
                "2022.04.10": ["IMG_20220410_105512.jpg"],
            },
        ),
        (
            ["IMG_20220410_105524.jpg", "IMG_20220410_143021.jpg"],
            {
                "2022.04.10": ["IMG_20220410_105524.jpg", "IMG_20220410_143021.jpg"],
            },
        ),
    ],
)
def test_get_photo_files_by_date(temp_dir, filenames, expected_result):
    # Arrange
    given_folder_contains_files(temp_dir, filenames)
    command = GetPhotosFromDirectory()

    # Act
    result = command(temp_dir)

    # Assert
    assert len(result) == len(expected_result)
    for date, files in expected_result.items():
        assert date in result
        assert sorted(result[date]) == sorted(files)

    assert result == expected_result


@pytest.mark.parametrize(
    "filenames, expected_structure",
    [
        (
            [],
            {},
        ),
        (
            [
                "IMG_20220305_132952.jpg",
                "IMG_20220306_143021.jpg",
                "IMG_20220410_105512.jpg",
            ],
            {
                "2022.03.05": ["IMG_20220305_132952.jpg"],
                "2022.03.06": ["IMG_20220306_143021.jpg"],
                "2022.04.10": ["IMG_20220410_105512.jpg"],
            },
        ),
        (
            ["IMG_20220410_105524.jpg", "IMG_20220410_143021.jpg"],
            {
                "2022.04.10": ["IMG_20220410_105524.jpg", "IMG_20220410_143021.jpg"],
            },
        ),
    ],
)
def test_move_files_to_folders_by_date(temp_dir, filenames, expected_structure):
    # Arrange
    given_folder_contains_files(temp_dir, filenames)

    # Act
    command = MoveFilesToFolders()
    command(temp_dir, expected_structure)

    # Assert
    # Check that files doesn't exist in parent folder
    assert os.listdir(temp_dir) == list(expected_structure.keys())
    # Check that files are moved to the correct folders
    for date, files in expected_structure.items():
        for filename in files:
            src_path = os.path.join(temp_dir, date, filename)
            assert os.path.exists(src_path)
