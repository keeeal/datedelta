
from dataclasses import dataclass
from typing import Any


DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _is_leap(year: int) -> bool:
    """Returns True if 'year' is a leap year, otherwise returns False."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_in_month(year: int, month: int) -> int:
    """Returns the number of days in a given month."""
    return DAYS_IN_MONTH[month - 1] + int(month == 2 and _is_leap(year))


@dataclass(frozen=True)
class Date:
    """Represents a date in the Gregorian calendar.

    A ``ValueError`` is raised if the date is invalid at initialization.

    Parameters
    ----------
    year : `int`
        The year. Can be positive or negative.
    month : `int`
        An integer in the range [1, 12], where 1 represents January.
    day : `int`
        The day of the given month, starting at 1.
    """

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        int_fields = self.year, self.month, self.day

        if not all(isinstance(i, int) for i in int_fields):
            raise ValueError("Integer argument expected")

        if not self._is_valid():
            raise ValueError(f"Invalid date: '{self}'")

    def __sub__(self, other: Any) -> int:
        """Calculate the difference between this date and another.

        The difference is defined as the absolute number of days found in
        between the two dates, not including the dates themselves.
        """

        if not isinstance(other, Date):
            return NotImplemented

        return max(abs(self.to_ordinal() - other.to_ordinal()) - 1, 0)

    @classmethod
    def from_isoformat(cls, date_string: str, /, sep: str = "-") -> "Date":
        """Construct a date by parsing a string of the form ``YYYY-MM-DD``.

        A ``ValueError`` is raised if the string is invalid.

        Parameters
        ----------
        date_string : `str`
            The string to parse containing the date in isoformat.
        sep : `str` (optional)
            The character used to delineate the numerical parts of the string.
            Default: "-".
        """

        # Define isoformat by creating a list of functions used to check each
        # character of the date string for validity.
        isoformat = 10 * [str.isdigit]
        isoformat[4] = isoformat[7] = lambda char: char == sep

        try:
            assert len(date_string) == len(isoformat)
            assert all(f(char) for f, char in zip(isoformat, date_string))
        except AssertionError:
            raise ValueError(f"Invalid date string: '{date_string}'")

        return Date(
            year=int(date_string[0:4]),
            month=int(date_string[5:7]),
            day=int(date_string[8:10]),
        )

    def to_ordinal(self) -> int:
        """Return an ordinal number representing the given date, where the 1st
        of January in year 0 is defined to be day 0.
        """

        def days_in_month_this_year(month: int) -> int:
            return _days_in_month(self.year, month)

        # Count the number of days to the start of the year.
        ordinal = 365 * self.year

        # Correct for leap year days
        ordinal += self.year // 4 - self.year // 100 + self.year // 400

        # Add the number of days to the start of the month.
        ordinal += sum(map(days_in_month_this_year, range(1, self.month)))

        # Add the date and correcting for negative values.
        ordinal += self.day - int(self.year >= 0)

        return ordinal

    def _is_valid(self) -> bool:
        """Return True if the date is a valid combination of year, month, and
        day in the Gregorian calendar, otherwise return False."""

        if not 1 <= self.month <= 12:
            return False

        if not 1 <= self.day <= _days_in_month(self.year, self.month):
            return False

        return True
