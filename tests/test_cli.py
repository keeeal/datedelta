
from argparse import Namespace
import sys
from typing import Any, Callable, Union

import pytest
from _pytest.python_api import RaisesContext

from datedelta.__main__ import delta, main, parse_line
from tests.utils import return_or_raise


@pytest.mark.parametrize(
    "date_string_1, date_string_2, expected_result",
    [
        ("2021-12-01", "2017-12-14",                      1447),
        ( "2021-12-1", "2017-12-14", pytest.raises(ValueError)),
        ("2021x12-01", "2017-12-14", pytest.raises(ValueError)),
        ("2021-12y01", "2017-12-14", pytest.raises(ValueError)),
        ("202a-12-01", "2017-12-14", pytest.raises(ValueError)),
        ("202a-12-01", "2017-12-14", pytest.raises(ValueError)),
        ("2021-1b-01", "2017-12-14", pytest.raises(ValueError)),
        ("2021-12-0c", "2017-12-14", pytest.raises(ValueError)),
        ("2021-12-01",  "2017-12-4", pytest.raises(ValueError)),
        ("2021-12-01", "2017x12-14", pytest.raises(ValueError)),
        ("2021-12-01", "2017-12y14", pytest.raises(ValueError)),
        ("2021-12-01", "201a-12-14", pytest.raises(ValueError)),
        ("2021-12-01", "2017-1b-14", pytest.raises(ValueError)),
        ("2021-12-01", "2017-12-1c", pytest.raises(ValueError)),
    ]
)
def test_delta(
    date_string_1: str,
    date_string_2: str,
    expected_result: Union[int, RaisesContext[Any]],
) -> None:
    return_or_raise(expected_result, delta, date_string_1, date_string_2)


@pytest.mark.parametrize(
    "input_string, expected_result",
    [
        (           "",                           pytest.raises(SystemExit)),
        (        "foo",                           pytest.raises(SystemExit)),
        (    "foo bar", Namespace(date_string_1="foo", date_string_2="bar")),
        ("foo bar baz",                           pytest.raises(SystemExit)),
    ]
)
def test_parse_line(
    input_string: str,
    expected_result: Union[str, RaisesContext[Any]],
) -> None:
    return_or_raise(expected_result, parse_line, input_string)


@pytest.mark.parametrize(
    "input_string, expected_result",
    [
        ("2021-12-01 2017-12-14",                       ["1447", "\n"]),
        (                     "",            pytest.raises(SystemExit)),
        (                  "foo",            pytest.raises(SystemExit)),
        (              "foo bar", ["Invalid date string: 'foo'", "\n"]),
        (          "foo bar baz",            pytest.raises(SystemExit)),
    ]
)
def test_main_with_arguments(
    input_string: str,
    expected_result: Union[str, RaisesContext[Any]],
    capture_stdout: list[str],
) -> None:
    sys.argv = [sys.argv[0]] + input_string.split()
    return_or_raise(expected_result, lambda: main() or capture_stdout)


@pytest.mark.parametrize(
    "input_string, expected_result",
    [
        ("2021-12-01 2017-12-14",                       ["1447", "\n"]),
        (                  "foo",            pytest.raises(SystemExit)),
        (              "foo bar", ["Invalid date string: 'foo'", "\n"]),
        (          "foo bar baz",            pytest.raises(SystemExit)),
        (                 "exit",                                   []),
    ]
)
def test_main_in_interactive_mode(
    input_string: str,
    expected_result: Union[str, RaisesContext[Any]],
    set_input: Callable[[str], None],
    capture_stdout: list[str],
) -> None:
    sys.argv.append("-i")
    set_input([input_string])

    try:
        return_or_raise(expected_result, lambda: main() or capture_stdout)
    except StopIteration:
        pass
