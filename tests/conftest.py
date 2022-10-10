
from typing import Callable, Optional

import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture
def set_input(monkeypatch: MonkeyPatch) -> Callable[[str], None]:
    """Returns a function that sets sequential return values of input().

    Raises StopIteration if input() is called more times than specified.
    """

    def _set_input(lines: list[str], /) -> None:
        def _input(prompt: Optional[str] = None, /) -> str:
            for line in lines:
                yield line

        monkeypatch.setattr('builtins.input', _input().__next__)

    return _set_input


@pytest.fixture
def capture_stdout(monkeypatch: MonkeyPatch) -> list[str]:
    """Returns a list containing the contents of each write to stdout."""

    writes = []
    monkeypatch.setattr('sys.stdout.write', writes.append)

    return writes
