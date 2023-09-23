import os
import re
from collections import defaultdict
from typing import Dict, List


class GetFilesFromDirectory:
    VALID_PATTERN = re.compile(
        r"""
        (
            ^IMG_\d{8}_\d{6}\.jpg$   # Image pattern
            |               # OR
            ^VID_\d{8}_\d{6}\.mp4$   # Video pattern
        )
        """,
        re.VERBOSE,
    )

    def __call__(self, dir_path) -> Dict[str, List[str]]:
        files_by_date = defaultdict(list)
        for filename in os.listdir(dir_path):
            if not self.is_valid_filename(filename) or not self.is_file(
                dir_path, filename
            ):
                continue

            folder_name = self._prepare_destination_folder_name(filename)
            files_by_date[folder_name].append(filename)
        return files_by_date

    def is_valid_filename(self, filename: str) -> bool:
        return bool(self.VALID_PATTERN.match(filename))

    @staticmethod
    def is_file(dir_path, filename):
        return os.path.isfile(os.path.join(dir_path, filename))

    @staticmethod
    def _prepare_destination_folder_name(name: str) -> str:
        date_str = name[4:12]
        # Convert date to the desired format (YYYY.MM.DD)
        formatted_date = f"{date_str[:4]}.{date_str[4:6]}.{date_str[6:]}"
        return formatted_date
