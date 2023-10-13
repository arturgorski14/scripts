import pytest

from OrganizePhotos.file_types import (FileType, ImageFileType,
                                       PanoramaFileType, VideoFileType)


@pytest.mark.parametrize(
    "filename, file_type",
    [
        ("IMG_20220410_105512.jpg", ImageFileType),
        ("IMG_20231007_092456_1.jpg", ImageFileType),
        ("VID_20231106_105512.mp4", VideoFileType),
        ("VID_20230624_081450_1.mp4", VideoFileType),
        ("PANO_20230916_173156.jpg", PanoramaFileType),
    ],
)
def test_is_valid_filename_success(filename: str, file_type: FileType):
    assert file_type().is_valid_filename(
        filename
    ), f"{filename=} doesnt match pattern {file_type.pattern}"


@pytest.mark.parametrize(
    "filename",
    [
        "not_matching_filenames.jpg",
        "IM_20220410_105512.jpg",
        "IMM_20220410_105512.jpg",
        "IMMG_20220410_105512.jpg",
        "IMG_202220410_105512.jpg",
        "IMG_2020410_105512.jpg",
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
def test_is_valid_filename_failure_for_image_file_type(filename):
    assert ImageFileType().is_valid_filename(filename) is False


@pytest.mark.parametrize(
    "filename, file_type, expected_folder_name",
    [
        ("IMG_20220410_105512.jpg", ImageFileType, "2022.04.10"),
        ("IMG_20231007_092456_1.jpg", ImageFileType, "2023.10.07"),
        ("VID_20231106_105512.mp4", VideoFileType, "2023.11.06"),
        ("VID_20230624_081450_1.mp4", VideoFileType, "2023.06.24"),
        ("PANO_20230916_173156.jpg", PanoramaFileType, "2023.09.16"),
    ],
)
def test_prepare_destination_folder_name(
    filename: str, file_type: FileType, expected_folder_name: str
):
    assert expected_folder_name == file_type.prepare_destination_folder_name(filename)
