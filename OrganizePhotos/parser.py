import argparse


def setup_parser() -> argparse.PARSER:
    parser = argparse.ArgumentParser(
        prog="python organize_photos.py",
        description="""
            Organize your photos into folders by date.
            """,
    )
    parser.add_argument(
        "-d",
        "--directory_path",
        default=None,
        help="Full path to directory ex. C:\\Users\\User\\Photos",
    )
    return parser
