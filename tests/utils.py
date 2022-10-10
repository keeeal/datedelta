
from typing import Any, Callable, Union

from _pytest.python_api import RaisesContext


def return_or_raise(
    expected_result: Union[Any, RaisesContext[Any]],
    test_function: Callable[..., Any],
    /,
    *args: Any,
    **kwargs: Any,
) -> None:
    """Assert that either the expected value is returned or that the expected
    exception is raised.

    Parameters
    ----------
    expected_result : `Any | RaisesContext`
        The expected return value or RaisesContext for expected exceptions.
    test_function : `Callable`
        The function to check the return value of.
    *args, **kwargs : `Any`
        Arguments and keyword arguments passed to the test function.
    """

    if isinstance(expected_result, RaisesContext):
        with expected_result:
            test_function(*args, **kwargs)
    else:
        assert test_function(*args, **kwargs) == expected_result
