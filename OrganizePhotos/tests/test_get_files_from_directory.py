import pytest

from OrganizePhotos.file_types import (ImageFileType, PanoramaFileType,
                                       VideoFileType)
from OrganizePhotos.get_photos_from_directory import GetFilesFromDirectory
from OrganizePhotos.tests.conftest import given_folder_contains_files


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
        (
            ["PANO_20230916_173711.jpg", "PANO_20231001_192309.jpg"],
            {
                "2023.09.16": ["PANO_20230916_173711.jpg"],
                "2023.10.01": ["PANO_20231001_192309.jpg"],
            },
        ),
    ],
)
def test_get_photo_files_by_date(temp_dir, filenames, expected_result):
    # Arrange
    given_folder_contains_files(temp_dir, filenames)
    command = GetFilesFromDirectory(
        (ImageFileType(), VideoFileType(), PanoramaFileType())
    )

    # Act
    result = command(temp_dir)

    # Assert
    assert len(result) == len(expected_result)
    for date, files in expected_result.items():
        assert date in result
        assert sorted(result[date]) == sorted(files)

    assert result == expected_result
