
from argparse import ArgumentParser, Namespace

from datedelta.date import Date


def delta(date_string_1: str, date_string_2: str) -> int:
    """Calculate the number of days between two date strings.

    A ValueError is raised if a string is invalid.

    Parameters
    ----------
    date_string_1 : `str`
        The first string to parse containing the date in isoformat.
    date_string_2 : `str`
        The second string to parse containing the date in isoformat.
    """

    date_1 = Date.from_isoformat(date_string_1)
    date_2 = Date.from_isoformat(date_string_2)

    return date_1 - date_2


def parse_line(line: str) -> Namespace:
    """Parse a string for the arguments required to calculate the delta.

    Prints usage help to stdout and then exits if arguments cannot be found.

    Parameters
    ----------
    line : `str`
        The string to parse containing the arguments.
    """

    parser = ArgumentParser()
    parser.add_argument("date_string_1")
    parser.add_argument("date_string_2")

    return parser.parse_args(line.split())


def main() -> None:
    """The main entry point of the program."""

    parser = ArgumentParser()
    parser.add_argument("date_strings", nargs="*")
    parser.add_argument("-i", "--interactive", action="store_true")
    args = parser.parse_args()

    if args.interactive:
        while True:
            line = input()

            if line == "exit":
                return

            try:
                print(delta(**vars(parse_line(line))))
            except ValueError as error:
                print(error)
                return

    try:
        print(delta(**vars(parse_line(" ".join(args.date_strings)))))
    except ValueError as error:
        print(error)
        return


if __name__ == "__main__":
    main()
