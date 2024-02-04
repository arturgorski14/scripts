import argparse


def setup_parser() -> argparse.PARSER:
    parser = argparse.ArgumentParser(
        prog="python organize_photos.py",
        description="""
            Organize your photos into folders by date.
            """,
    )
    parser.add_argument(
        "-f",
        "--full-path",
        default=None,
        help="Full path to directory ex. C:\\Users\\User\\Photos",
    )
    parser.add_argument(
        "-a",
        "--aggregation",
        choices=["day", "month", "year"],
        default="day",
        help="Defines how to aggregate files."
             "By year -> aggregates by YYYY."
             "By month -> aggregates by YYYY.MM."
             "By day -> aggregates by YYYY.MM.DD."
             "Day is the default"
    )
    return parser
