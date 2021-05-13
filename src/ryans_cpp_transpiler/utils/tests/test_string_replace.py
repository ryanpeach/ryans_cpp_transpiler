import pytest

from src.ryans_cpp_transpiler.utils.exceptions import OverlapException
from src.ryans_cpp_transpiler.utils.string_replace import batch_string_replace


def test_batch_string_replace_overlap() -> None:
    """Tests that overlaps raise an exception."""
    with pytest.raises(OverlapException):
        batch_string_replace(
            text="asdfghjkl;", replacements=[((0, 2), "a"), ((1, 3), "b")]
        )


def test_batch_string_replace_single_same() -> None:
    """Tests a single replacement with same number of letters."""
    out = batch_string_replace(text="asdfghjkl;", replacements=[((0, 2), "xx")])
    assert out == "xxdfghjkl;"


def test_batch_string_replace_single_smaller() -> None:
    """Tests a single replacement with same number of letters."""
    out = batch_string_replace(text="asdfghjkl;", replacements=[((0, 2), "x")])
    assert out == "xdfghjkl;"


def test_batch_string_replace_single_bigger() -> None:
    """Tests a single replacement with same number of letters."""
    out = batch_string_replace(text="asdfghjkl;", replacements=[((0, 2), "xxx")])
    assert out == "xxxdfghjkl;"


def test_batch_string_replace_single_zero() -> None:
    """Tests a single replacement with same number of letters."""
    out = batch_string_replace(text="asdfghjkl;", replacements=[((0, 2), "")])
    assert out == "dfghjkl;"


def test_batch_string_replace_same() -> None:
    """Tests a single replacement with same number of letters."""
    out = batch_string_replace(
        text="asdfghjkl;", replacements=[((0, 2), "xx"), ((3, 5), "xx")]
    )
    assert out == "xxdxxhjkl;"


def test_batch_string_replace_smaller() -> None:
    """Tests a single replacement with same number of letters."""
    out = batch_string_replace(
        text="asdfghjkl;", replacements=[((0, 2), "x"), ((3, 5), "xx")]
    )
    assert out == "xdxxhjkl;"


def test_batch_string_replace_bigger() -> None:
    """Tests a single replacement with same number of letters."""
    out = batch_string_replace(
        text="asdfghjkl;", replacements=[((0, 2), "xxx"), ((3, 5), "xx")]
    )
    assert out == "xxxdxxhjkl;"
