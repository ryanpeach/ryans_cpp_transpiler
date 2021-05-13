from typing import NewType, Tuple

from iregex import Regex

#: Represents an index in the original string.
OriginalIdx = NewType("OriginalIdx", int)

#: Represents an index in a partial section of the original string.
PartialIdx = NewType("PartialIdx", int)

#: Represents a slice in the original index. Uses inclusive start index and exclusive end index.
OriginalSlice = Tuple[OriginalIdx, OriginalIdx]

#: Represents a slice in the partial index. Uses inclusive start index and exclusive end index.
PartialSlice = Tuple[PartialIdx, PartialIdx]

#: Represents the original text.
OriginalTxt = NewType("OriginalTxt", str)

#: Represents a partial section of the original text.
PartialTxt = NewType("PartialTxt", str)

#: Represents a partial section of the original text with converted elements in it.
ConvertedPartialTxt = NewType("ConvertedPartialTxt", str)

#: Represents the full converted text.
ConvertedTxt = NewType("ConvertedTxt", str)


class HasContext:
    """Provides a context object that narrows down the search for the local regex."""

    #: Used to filter the string into PartialTxt type before passing to underlying methods.
    context: Regex = Regex().anything()


class Complaint(str):
    """A single complaint. Made a class for future proofing."""

    #: The string representation of this complaint
    _str: str

    #: The slice in the original text of this complaint
    _original_slice: OriginalSlice

    def __init__(
        self, sl: OriginalSlice, original_text: OriginalTxt, complaint_txt: str
    ) -> None:
        """
        Basic init saving the slice and a string representation of the complaint.

        TODO: Make this more complicated for better formatting of complaint messages.
        """
        self._original_slice = sl
        self._str = f"{sl}: {original_text[sl[0]:sl[1]]}\nComplaint: {complaint_txt}"

    def __str__(self) -> str:
        return self._str

    def __repr__(self) -> str:
        return self._str
