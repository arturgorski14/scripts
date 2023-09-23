import argparse
import os

from OrganizePhotos.get_photos_from_directory import GetPhotosFromDirectory
from OrganizePhotos.move_files_to_folders import MoveFilesToFolders

CONFIG_FILE = f"organize_photos_config.ini"


# TODO: Write missing tests
# TODO: Clean main function
# TODO: print -> logger
# TODO: progressbar


def save_then_get_last_used_directory(dir_path) -> str | None:
    if dir_path:
        with open(CONFIG_FILE, "w") as conf:
            conf.write(dir_path)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as conf:
            return conf.read()


def organize_photos() -> None:
    parser = argparse.ArgumentParser(
        prog="python organize_photos.py",
        description="""
        Organize your photos into folders by date.
        First use? Pass the full path to the photo directory in the directory_path parameter.
        The script saves the last used folder and will use it next time :)
        """,
    )
    parser.add_argument(
        "-d",
        "--directory_path",
        default="",
        required=False,
    )
    args = parser.parse_args()

    source_directory_path = save_then_get_last_used_directory(args.directory_path)
    if not source_directory_path:
        parser.print_help()
        return

    get_data_command = GetPhotosFromDirectory()
    all_photo_files_by_date = get_data_command(source_directory_path)
    print(all_photo_files_by_date)
    move_files_command = MoveFilesToFolders()
    move_files_command(source_directory_path, all_photo_files_by_date)
    print("Files moving finished!")


if __name__ == "__main__":
    organize_photos()
