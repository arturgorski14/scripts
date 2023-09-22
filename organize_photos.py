import re
import os
import shutil
from collections import defaultdict
from typing import Dict, List

FOLDER_NAME_WITH_PHOTOS = r"C:\Users\Artur\Pictures\Screenshots\Z_telefonu"


def main() -> None:
    all_photo_files_by_date = get_photo_files_by_date(FOLDER_NAME_WITH_PHOTOS)
    print(all_photo_files_by_date)
    move_files_to_folders_by_date(FOLDER_NAME_WITH_PHOTOS, all_photo_files_by_date)


def get_photo_files_by_date(dirpath: str) -> Dict[str, List[str]]:
    photo_files_by_date = defaultdict(list)
    for filename in os.listdir(dirpath):  # filename is IMG_20220305_132952.jpg
        fullpath = os.path.join(dirpath, filename)

        # Check if the item is a file
        if not os.path.isfile(fullpath):
            continue

        # Extract the date from the filename (assuming the format is IMG_YYYYMMDD_...)
        date_str = filename[4:12]

        # Convert date to the desired format (YYYY.MM.DD)
        formatted_date = f"{date_str[:4]}.{date_str[4:6]}.{date_str[6:]}"

        # Append the file's full path to the list for that date
        photo_files_by_date[formatted_date].append(filename)
    return photo_files_by_date


def move_files_to_folders_by_date(dirpath: str, files: Dict[str, List[str]]) -> None:
    for date, files_by_date in files.items():
        new_folder_path = os.path.join(dirpath, date)

        # Use os.makedirs to create parent directories if they don't exist
        os.makedirs(new_folder_path, exist_ok=True)

        for filename in files_by_date:
            src_path = os.path.join(dirpath, filename)
            dest_path = os.path.join(new_folder_path, filename)

            # Use shutil.move for safer file moving (handles errors better)
            try:
                shutil.move(src_path, dest_path)
                print(f"{src_path} -> {dest_path}")
            except Exception as e:
                print(f"Error moving '{src_path}' to '{dest_path}': {e}")


filename_pattern = re.compile(r'^IMG_\d{8}_\d{6}\.jpg$')


def is_valid_filename(filename):
    # Use the precompiled pattern to check if the filename matches
    return bool(filename_pattern.match(filename))


if __name__ == "__main__":
    main()
