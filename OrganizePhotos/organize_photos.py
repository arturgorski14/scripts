import logging
import sys
from parser import setup_parser

from file_types import ImageFileType, PanoramaFileType, VideoFileType
from get_photos_from_directory import GetFilesFromDirectory
from move_files_to_folders import (MoveFilesToParentDirectories,
                                   MoveFilesToSubdirectories)


def organize_photos(dir_path) -> None:
    get_data_command = GetFilesFromDirectory(
        (ImageFileType(), VideoFileType(), PanoramaFileType())
    )
    all_photo_files_by_date = get_data_command(dir_path)
    logger.debug(all_photo_files_by_date)
    move_files_command = MoveFilesToSubdirectories()
    move_files_command(dir_path, all_photo_files_by_date)
    logger.info("Files moving finished!")


def organize_photos2(dir_path) -> None:
    move_files_command = MoveFilesToParentDirectories()
    move_files_command(dir_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = setup_parser()
    args = parser.parse_args()
    if not args.full_path:
        parser.print_help()
        exit()

    organize_photos(args.full_path)
