import logging
import os
from collections import defaultdict
from typing import Dict, Iterable, List

from tqdm import tqdm


class GetFilesFromDirectory:
    def __init__(self, valid_types: Iterable = None):
        if not valid_types:
            valid_types = []
        self.VALID_TYPES = valid_types

    def __call__(self, dir_path) -> Dict[str, List[str]]:
        files_by_date = defaultdict(list)
        filenames = os.listdir(dir_path)
        logging.info(f"Found {len(filenames)} inside {dir_path}")
        valid_files = 0

        for filename in tqdm(filenames, desc="Processing Files"):
            if not self.is_file(dir_path, filename):
                continue
            for file_type in self.VALID_TYPES:
                if not file_type.is_valid_filename(filename):
                    continue
                folder_name = file_type.prepare_destination_folder_name(filename)
                files_by_date[folder_name].append(filename)
                valid_files += 1
        logging.info(f"Moved {valid_files} in total")
        return files_by_date

    @staticmethod
    def is_file(dir_path, filename):
        return os.path.isfile(os.path.join(dir_path, filename))
