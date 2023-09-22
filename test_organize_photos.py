import os
import tempfile

import pytest
from organize_photos import get_photo_files_by_date, move_files_to_folders_by_date


# Define a fixture to create a temporary directory for testing
@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


def given_folder_contains_files(dir_path, filenames):
    for filename in filenames:
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "w") as f:
            f.write("Sample file content")
    assert os.listdir(dir_path) == filenames, "ERROR: INCORRECTLY PREPARED DATA!"


@pytest.mark.parametrize(
    "filenames, expected_result",
    [
        (
          [],
          {},
        ),
        (
            ["IMG_20220305_132952.jpg", "IMG_20220306_143021.jpg", "IMG_20220410_105512.jpg"],
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

    # Act
    result = get_photo_files_by_date(temp_dir)

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
            ["IMG_20220305_132952.jpg", "IMG_20220306_143021.jpg", "IMG_20220410_105512.jpg"],
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
    move_files_to_folders_by_date(temp_dir, expected_structure)

    # Assert
    # Check that files doesn't exist in parent folder
    assert os.listdir(temp_dir) == list(expected_structure.keys())
    # Check that files are moved to the correct folders
    for date, files in expected_structure.items():
        for filename in files:
            src_path = os.path.join(temp_dir, date, filename)
            assert os.path.exists(src_path)
