import os
from typing import List, Tuple

from ryans_cpp_transpiler.utils.exceptions import OverlapException
from ryans_cpp_transpiler.utils.types import (
    ConvertedPartialTxt,
    FormattedTxt,
    OriginalIdx,
    OriginalSlice2,
    OriginalTxt,
    OutputTxt,
)


def batch_string_replace(
    text: OriginalTxt, replacements: List[Tuple[OriginalSlice2, ConvertedPartialTxt]]
) -> OutputTxt:
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

    return "".join(new_char_list)


def make_inline_record_index(
    text: OriginalTxt,
) -> Tuple[List[OriginalIdx], FormattedTxt]:
    """
    Removes newline whitespace and comments then records an
    index list so you can recover the indexes from the old text.

    The output contains two variables:
    0: A list of integers whos i'th value indicates the index in `text`
       where the second variables i'th value came from.
    1: A new string.
    """
    # Some constants to keep track of
    linesep_len = len(os.linesep)
    split_newlines = text.splitlines()

    # The variables we will edit
    out_idxs: List[int] = []
    out_idx = 0
    out_str_list: List[str] = []

    # Iterate over the lines
    for line_num, line in enumerate(split_newlines):
        # If there is an inline comment we need to strip it out to remain whitespace agnostic
        if "//" in line:
            end_of_line = line.index("//")
            stripped_of_inline_comments = line[:end_of_line]
            out_str_list += stripped_of_inline_comments
            out_idxs += list(range(out_idx, out_idx + len(stripped_of_inline_comments)))
            out_idx += len(stripped_of_inline_comments)
            out_idx += len(line) - end_of_line

        # Otherwise things are much easier
        else:
            out_str_list += line
            out_idxs += list(range(out_idx, out_idx + len(line)))
            out_idx += len(line)

        out_idx += linesep_len

    return out_idxs, "".join(out_str_list)
