from typing import NewType, Tuple

FormattedIdx = NewType("FormattedIdx", int)
OriginalIdx = NewType("OriginalIdx", int)
Slice2 = Tuple[
    int, int
]  # Prevents slices with a step in them. The second element is exclusive.
OriginalSlice2 = Tuple[OriginalIdx, OriginalIdx]
FormattedSlice2 = Tuple[FormattedIdx, FormattedIdx]
OriginalTxt = NewType("OriginalTxt", str)
FormattedTxt = NewType("FormattedTxt", str)
ConvertedPartialTxt = NewType("ConvertedPartialTxt", str)
OutputTxt = NewType("OutputTxt", str)
