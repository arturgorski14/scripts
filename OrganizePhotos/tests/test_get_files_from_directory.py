import re
from typing import Pattern

import pytest

from OrganizePhotos.get_photos_from_directory import GetFilesFromDirectory
from OrganizePhotos.tests.conftest import given_folder_contains_files

EXPECTED_IMAGE_PATTERN: Pattern[str] = re.compile(r"^IMG_\d{8}_\d{6}\.jpg$")
EXPECTED_VIDEO_PATTERN: Pattern[str] = re.compile(r"^VID_\d{8}_\d{6}\.mp4$")
EXPECTED_PANORAMA_PATTERN: Pattern[str] = re.compile(r"^PANO_\d{8}_\d{6}\.jpg$")


@pytest.mark.parametrize(
    "filename, expected_pattern",
    [
        ("IMG_20220410_105512.jpg", EXPECTED_IMAGE_PATTERN),
        ("VID_20231106_105512.mp4", EXPECTED_VIDEO_PATTERN),
        ("PANO_20230916_173156.jpg", EXPECTED_PANORAMA_PATTERN),
    ],
)
def test_is_valid_filename_success(filename, expected_pattern):
    command = GetFilesFromDirectory()
    assert (
        command.is_valid_filename(filename) is True
    ), f"{filename=} doesnt match pattern {expected_pattern}"


@pytest.mark.parametrize(
    "folder_name_matching_pattern",
    [
        "IMG_20220305_132952.jpg",
        "VID_20220305_132952.mp4",
        "PANO_20231001_192309.jpg",
    ],
)
def test_validate_file_with_folder_name(tmpdir, folder_name_matching_pattern):
    # Validate the folder name
    command = GetFilesFromDirectory()
    is_valid_file = command.is_file(tmpdir, folder_name_matching_pattern)
    is_valid_pattern = command.is_valid_filename(folder_name_matching_pattern)

    # Check that the folder name is considered invalid because it matches the pattern
    assert (
        not is_valid_file and is_valid_pattern
    ), f"Folder shouldn't be allowed! {is_valid_file=}, {is_valid_pattern=}"


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
        "IIMG_20220410_105512.jpg",
        "IMG_20220410_105512.jpgg",
        "IMG_20220410_105512.mp4",
        "IMG_20220410_105512.png",
        "IMG_20220410_105512.webp",
        "IMG_20220410_105512.jpeg",
        "IMG_20220410_105512.csv",
        "not_matching_filenames.mp4",
        "VI_20220410_105512.mp4",
        "VII_20220410_105512.mp4",
        "VIID_20220410_105512.mp4",
        "VID_202220410_105512.mp4",
        "VID_2020410_105512.mp4",
        "VID_20220410_1055512.mp4",
        "VID_20220410_10512.mp4",
        "VID_VID_20220410_105512.mp4",
        "VID_20220410_105512.jpgg",
        "IIMG_20220410_105512.jpg",
        "VID_20220410_105512.mp44",
        "VID_20220410_105512.jpg",
        "VID_20220410_105512.png",
        "VID_20220410_105512.webp",
        "VID_20220410_105512.jpeg",
        "VID_20220410_105512.csv",
        "PAN0_20220410_105512.jpg",
        "PANOO_20220410_105512.jpg",
        "PANOR_20220410_105512.jpg",
        "PANO_202220410_105512.jpg",
        "PANO_2020410_105512.jpg",
        "PANO_20220410_1055512.jpg",
        "PANO_20220410_10512.jpg",
        "PANO_PANO_20220410_105512.jpg",
        "PANO_20220410_105512.jpgg",
        "IIMG_20220410_105512.jpg",
        "PANO_20220410_105512.jpgg",
        "PANO_20220410_105512.mp4",
        "PANO_20220410_105512.png",
        "PANO_20220410_105512.webp",
        "PANO_20220410_105512.jpeg",
        "PANO_20220410_105512.csv",
    ],
)
def test_is_valid_filename_failure(filename):
    command = GetFilesFromDirectory()
    assert command.is_valid_filename(filename) is False


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
    command = GetFilesFromDirectory()

    # Act
    result = command(temp_dir)

    # Assert
    assert len(result) == len(expected_result)
    for date, files in expected_result.items():
        assert date in result
        assert sorted(result[date]) == sorted(files)

    assert result == expected_result
