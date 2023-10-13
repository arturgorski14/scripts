import logging
from parser import setup_parser

from file_types import ImageFileType, PanoramaFileType, VideoFileType
from get_photos_from_directory import GetFilesFromDirectory
from move_files_to_folders import MoveFilesToFolders


def organize_photos() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = setup_parser()
    args = parser.parse_args()
    if not args.directory_path:
        parser.print_help()
        return

    get_data_command = GetFilesFromDirectory(
        (ImageFileType(), VideoFileType(), PanoramaFileType())
    )
    all_photo_files_by_date = get_data_command(args.directory_path)
    logger.debug(all_photo_files_by_date)
    move_files_command = MoveFilesToFolders()
    move_files_command(args.directory_path, all_photo_files_by_date)
    logger.info("Files moving finished!")


if __name__ == "__main__":
    organize_photos()
