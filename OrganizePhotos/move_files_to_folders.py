import os
import shutil
from typing import Dict, List


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
