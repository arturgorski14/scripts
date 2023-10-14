import re
from abc import ABC
from typing import Pattern


# TODO: more dynamic patterns (allow other date formats)

class FileType(ABC):
    pattern: Pattern[str]

    @staticmethod
    def prepare_destination_folder_name(name: str) -> str:
        raise NotImplementedError

    def is_valid_filename(self, filename: str) -> bool:
        return bool(self.pattern.match(filename))


class ImageFileType(FileType):
    pattern: Pattern[str] = re.compile(r"^IMG_\d{8}_.*\.jpg$")

    @staticmethod
    def prepare_destination_folder_name(name: str) -> str:
        date_str = name[4:12]
        # Convert date to the desired format (YYYY.MM.DD)
        formatted_date = f"{date_str[:4]}.{date_str[4:6]}.{date_str[6:]}"
        return formatted_date


class VideoFileType(FileType):
    pattern: Pattern[str] = re.compile(r"^VID_\d{8}_.*\.mp4$")

    @staticmethod
    def prepare_destination_folder_name(name: str) -> str:
        date_str = name[4:12]
        # Convert date to the desired format (YYYY.MM.DD)
        formatted_date = f"{date_str[:4]}.{date_str[4:6]}.{date_str[6:]}"
        return formatted_date


class PanoramaFileType(FileType):
    pattern: Pattern[str] = re.compile(r"^PANO_\d{8}_.*\.jpg$")

    @staticmethod
    def prepare_destination_folder_name(name: str) -> str:
        date_str = name[5:13]
        # Convert date to the desired format (YYYY.MM.DD)
        formatted_date = f"{date_str[:4]}.{date_str[4:6]}.{date_str[6:]}"
        return formatted_date
