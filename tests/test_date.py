
from dataclasses import dataclass
from operator import sub
from typing import Any, Union

import pytest
from _pytest.python_api import RaisesContext

from datedelta.date import Date, _days_in_month, _is_leap
from tests.utils import return_or_raise


@dataclass
class MockDateFields:
    year: int
    month: int
    day: int


@pytest.mark.parametrize(
    "test_year, expected_result",
    [
        (1993, False),  # Not divisible by 4
        (2020, True),   # Divisible by 4
        (1900, False),  # Divisible by 100
        (2000, True),   # Divisible by 400
    ]
)
def test_is_leap(
    test_year: int,
    expected_result: bool,
) -> None:
    assert _is_leap(test_year) == expected_result


@pytest.mark.parametrize(
    "test_year, test_month, expected_result",
    [
        (1993, 7, 31),  # Non-leap year, not February
        (2000, 7, 31),  # Leap year, not February
        (1993, 2, 28),  # Non-leap year, February
        (2000, 2, 29),  # Leap year, February
    ]
)
def test_days_in_month(
    test_year: int,
    test_month: int,
    expected_result: int,
) -> None:
    assert _days_in_month(test_year, test_month) == expected_result


@pytest.mark.parametrize(
    "test_year, test_month, test_day, expected_result",
    [
        ( 1993,  7, 13,  True),  # Valid date
        ( 1993,  0, 13, False),  # Month < 1
        ( 1993, 13, 13, False),  # Month > 12
        ( 1993,  7,  0, False),  # Day < 1
        ( 1993,  7, 32, False),  # Day > days in month
        ( 2020,  2, 29,  True),  # Valid leap date
        ( 1993,  2, 29, False),  # Invalid leap date
    ]
)
def test_is_valid(
    test_year: int,
    test_month: int,
    test_day: int,
    expected_result: bool,
) -> None:
    date_fields = MockDateFields(test_year, test_month, test_day)
    assert Date._is_valid(date_fields) == expected_result


@pytest.mark.parametrize(
    "test_year, test_month, test_day, expected_result",
    [
        ( 1993,  7, 13,         Date(1993, 7, 13)),  # Valid date
        ( 1993,  0, 13, pytest.raises(ValueError)),  # Month < 1
        ( 1993, 13, 13, pytest.raises(ValueError)),  # Month > 12
        ( 1993,  7,  0, pytest.raises(ValueError)),  # Day < 1
        ( 1993,  7, 32, pytest.raises(ValueError)),  # Day > days in month
        ( 2020,  2, 29,         Date(2020, 2, 29)),  # Valid leap date
        ( 1993,  2, 29, pytest.raises(ValueError)),  # Invalid leap date
    ]
)
def test_post_init(
    test_year: int,
    test_month: int,
    test_day: int,
    expected_result: Union[Date, RaisesContext[Any]],
) -> None:
    return_or_raise(expected_result, Date, test_year, test_month, test_day)


@pytest.mark.parametrize(
    "test_string, expected_result",
    [
        ( "1993-07-13",         Date(1993, 7, 13)),
        (  "1993-7-13", pytest.raises(ValueError)),
        ("1993-007-13", pytest.raises(ValueError)),
        ( "1993x07-13", pytest.raises(ValueError)),
        ( "1993-07y13", pytest.raises(ValueError)),
        ( "199a-07-13", pytest.raises(ValueError)),
        ( "1993-0b-13", pytest.raises(ValueError)),
        ( "1993-07-1c", pytest.raises(ValueError)),
    ]
)
def test_from_isoformat(
    test_string: str,
    expected_result: Union[Date, RaisesContext[Any]],
) -> None:
    return_or_raise(expected_result, Date.from_isoformat, test_string)


@pytest.mark.parametrize(
    "test_year, test_month, test_day, expected_result",
    [
        (  -1, 12, 31,     -1),
        (   0,  1,  1,      0),
        (1993,  7, 13, 728121),
    ]
)
def test_to_ordinal(
    test_year: int,
    test_month: int,
    test_day: int,
    expected_result: int,
) -> None:
    assert Date(test_year, test_month, test_day).to_ordinal() == expected_result


@pytest.mark.parametrize(
    "test_date_1, test_date_2, expected_result",
    [
        (Date(1993, 7, 13), Date(1993, 7, 11), 1),
        (Date(1993, 7, 13), Date(1993, 7, 12), 0),
        (Date(1993, 7, 13), Date(1993, 7, 13), 0),
        (Date(1993, 7, 13), Date(1993, 7, 14), 0),
        (Date(1993, 7, 13), Date(1993, 7, 15), 1),
        (Date(1993, 7, 13), "Not a date", pytest.raises(TypeError)),
    ]
)
def test_subtraction_operator(
    test_date_1: Date,
    test_date_2: Date,
    expected_result: Union[int, RaisesContext[Any]],
) -> None:
    return_or_raise(expected_result, sub, test_date_1, test_date_2)
