import argparse
from unittest import mock

import pytest

from OrganizePhotos.organize_photos import main
from OrganizePhotos.parser import setup_parser


def test_setup_parser_default_values():
    parser = setup_parser()
    args = parser.parse_args([])

    assert args.full_path is None
    assert args.aggregation == "day"


def test_setup_parser_full_path():
    parser = setup_parser()
    args = parser.parse_args(["-f", "C:\\Users\\User\\Photos"])

    assert args.full_path == "C:\\Users\\User\\Photos"
    assert args.aggregation == "day"


def test_setup_parser_aggregation():
    parser = setup_parser()
    args = parser.parse_args(["-a", "month"])

    assert args.full_path is None
    assert args.aggregation == "month"


def test_setup_parser_invalid_aggregation():
    parser = setup_parser()
    with pytest.raises(
        SystemExit
    ):  # argparse wywoła SystemExit przy nieprawidłowym argumencie
        parser.parse_args(["-a", "invalid"])


def test_setup_parser_all_args():
    parser = setup_parser()
    args = parser.parse_args(["-f", "C:\\Users\\User\\Photos", "-a", "year"])

    assert args.full_path == "C:\\Users\\User\\Photos"
    assert args.aggregation == "year"
