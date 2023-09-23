import os
import re
from collections import defaultdict
from typing import Pattern, Dict, List


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
