from typing import NewType, Tuple

OriginalIdx = NewType("OriginalIdx", int)
FormattedIdx = NewType("FormattedIdx", int)
FormattedPartialIdx = NewType("FormattedPartialIdx", int)

Slice2 = Tuple[
    int, int
]  # Prevents slices with a step in them. The second element is exclusive.
OriginalSlice2 = Tuple[OriginalIdx, OriginalIdx]
FormattedSlice2 = Tuple[FormattedIdx, FormattedIdx]
FormattedPartialSlice2 = Tuple[FormattedPartialIdx, FormattedPartialIdx]

OriginalTxt = NewType("OriginalTxt", str)
FormattedTxt = NewType("FormattedTxt", str)
FormattedPartialTxt = NewType("FormattedPartialTxt", str)
ConvertedPartialTxt = NewType("ConvertedPartialTxt", str)
OutputTxt = NewType("OutputTxt", str)
