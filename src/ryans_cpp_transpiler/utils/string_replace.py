import os
from typing import List, Tuple

from src.ryans_cpp_transpiler.utils.exceptions import OverlapException
from src.ryans_cpp_transpiler.utils.types import (
    ConvertedPartialTxt,
    ConvertedTxt,
    OriginalSlice,
    OriginalTxt,
)


def batch_string_replace(
    text: OriginalTxt, replacements: List[Tuple[OriginalSlice, ConvertedPartialTxt]]
) -> ConvertedTxt:
    """Replaces a batch of string elements in O(N) time."""

    # Sanity check the replacements for overlaps
    k_ = 0
    for (j, k), __ in sorted(replacements):
        if j < k_:
            raise OverlapException("Replacements should not overlap.")
        k_ = k

    # Make the character replacements
    old_char_list = list(text)
    old_char_list_idx = 0
    new_char_list: List[str] = []
    for (j, k), new_txt in sorted(replacements):
        # First go over the text we have ignored so far
        new_char_list += old_char_list[old_char_list_idx:j]
        old_char_list_idx += j - old_char_list_idx

        # Now lets add the replacement text
        new_char_list += new_txt

        # Now lets make the old_char_list_idx the end of the replaced string
        old_char_list_idx = k

    # Now for the end of the string
    new_char_list += old_char_list[old_char_list_idx:]

    return ConvertedTxt("".join(new_char_list))
