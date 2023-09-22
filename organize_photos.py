import argparse
import re
import os
import shutil
from collections import defaultdict
from typing import Dict, List, Pattern

CONFIG_FILE = f"organize_photos_config.ini"


# TODO: Change language to English
# TODO: Separate code
# TODO: Clean main function
# TODO: Write missing tests

class GetPhotosFromDirectory:
    VALID_FILENAME_PATTERN: Pattern[str] = re.compile(r"^IMG_\d{8}_\d{6}\.jpg$")

    def __call__(self, dir_path) -> Dict[str, List[str]]:
        photo_files_by_date = defaultdict(list)
        for filename in os.listdir(dir_path):
            if not self.validate_filename(filename):
                continue

            folder_name = self._prepare_destination_folder_name(filename)
            photo_files_by_date[folder_name].append(filename)
        return photo_files_by_date

    def validate_filename(self, filename: str) -> bool:
        # TODO: possible case of folder named with correct pattern
        return bool(self.VALID_FILENAME_PATTERN.match(filename))

    @staticmethod
    def _prepare_destination_folder_name(name: str) -> str:
        date_str = name[4:12]
        # Convert date to the desired format (YYYY.MM.DD)
        formatted_date = f"{date_str[:4]}.{date_str[4:6]}.{date_str[6:]}"
        return formatted_date


class MoveFilesToFolders:
    def __call__(self, dir_path: str, data: Dict[str, List[str]]) -> None:
        for folder_name, filenames in data.items():
            new_folder_path = os.path.join(dir_path, folder_name)

            # Use os.makedirs to create parent directories if they don't exist
            os.makedirs(new_folder_path, exist_ok=True)

            for filename in filenames:
                src_path = os.path.join(dir_path, filename)
                destination_path = os.path.join(new_folder_path, filename)
                self.move_file(src_path, destination_path)

    @staticmethod
    def move_file(src: str, destination: str):
        # Use shutil.move for safer file moving (handles errors better)
        try:
            shutil.move(src, destination)
            print(f"{src} -> {destination}")
        except Exception as e:
            print(f"Error moving '{src}' to '{destination}': {e}")


def save_then_get_last_used_directory(dir_path) -> str:
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
        Zorganizuj swoje zdjęcia w folderach po datach.
        Pierwsze użycie? Przekaż w parametrze directory_path pełną ścieżkę do katalogu ze zdjęciami.
        Skrypt zapisuje ostatnio wykorzystany folder, przy kolejnym użyciu wykorzysta go :)
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
    print("Wszystkie pliki zostały przeniesione :)")


if __name__ == "__main__":
    organize_photos()
