import re
from typing import Pattern

import pytest

from OrganizePhotos.get_photos_from_directory import GetPhotosFromDirectory
from OrganizePhotos.tests.conftest import given_folder_contains_files

EXPECTED_FILENAME_PATTERN: Pattern[str] = re.compile(r"^IMG_\d{8}_\d{6}\.jpg$")


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


# TODO: consider separating tests for incorrect image names
