import os

import pytest

from OrganizePhotos.move_files_to_folders import MoveFilesToFolders
from OrganizePhotos.tests.conftest import given_folder_contains_files


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
        (
            ["PANO_20230916_173711.jpg", "PANO_20231001_192309.jpg"],
            {
                "2023.09.16": ["PANO_20230916_173711.jpg"],
                "2023.10.01": ["PANO_20231001_192309.jpg"],
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
