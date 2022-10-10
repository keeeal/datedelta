
from argparse import ArgumentParser
from datedelta.date import Date


def print_delta(first_date: str, second_date: str) -> None:
    print(Date.from_isoformat(first_date) - Date.from_isoformat(second_date))


def cli() -> None:
    parser = ArgumentParser()
    parser.add_argument("first_date")
    parser.add_argument("second_date")

    print_delta(**vars(parser.parse_args()))
