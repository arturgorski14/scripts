import logging
import os
import shutil
from typing import Dict, List


class MoveFilesToSubdirectories:
    def __call__(self, dir_path: str, data: Dict[str, List[str]]) -> None:
        for folder_name, filenames in data.items():
            new_folder_path = os.path.join(dir_path, folder_name)

            # Use os.makedirs to create parent directories if they don't exist
            os.makedirs(new_folder_path, exist_ok=True)

            for filename in filenames:
                src_path = os.path.join(dir_path, filename)
                destination_path = os.path.join(new_folder_path, filename)
                self._move_file(src_path, destination_path)

    @staticmethod
    def _move_file(src: str, destination: str):
        # Use shutil.move for safer file moving (handles errors better)
        try:
            shutil.move(src, destination)
            logging.debug(f"{src} -> {destination}")
        except Exception as e:
            logging.error(f"Error moving '{src}' to '{destination}': {e}")


class MoveFilesToParentDirectories:

    def __call__(self, dir_path: str) -> None:
        self._move_files(dir_path)
        self._remove_empty_directory(dir_path)

    @staticmethod
    def _move_files(src_dir: str):
        destination_dir = os.path.dirname(src_dir)
        # Use shutil.move for safer file moving (handles errors better)
        for filename in os.listdir(src_dir):
            file_src_path = os.path.join(src_dir, filename)
            file_destination_path = os.path.join(destination_dir, filename)
            try:
                shutil.move(file_src_path, file_destination_path)
                logging.debug(f"{file_src_path} -> {file_destination_path}")
            except Exception as e:
                logging.error(f"Error moving '{file_src_path}' to '{file_destination_path}': {e}")

    @staticmethod
    def _remove_empty_directory(dir_path):
        if not len(os.listdir(dir_path)):
            os.rmdir(dir_path)
