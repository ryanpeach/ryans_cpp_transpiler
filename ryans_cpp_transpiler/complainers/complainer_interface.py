from typing import List, Optional

from iregex import Regex

from ryans_cpp_transpiler.utils.types import (
    FormattedSlice2,
    FormattedTxt,
    OriginalIdx,
    OriginalSlice2,
    OriginalTxt,
)


class Complaint(str):
    """A single complaint. Made a class for future proofing."""

    pass


class Complainer:
    """Shows errors when it finds specific strings."""

    context: Optional[Regex]

    @staticmethod
    def _complain(sl: OriginalSlice2, text: OriginalTxt) -> Complaint:
        """Returns a string to printout describing the complaint."""
        raise NotImplementedError("Needs to be implemented.")

    def find(self: "Complainer", text: FormattedTxt) -> List[FormattedSlice2]:
        """Returns a list of slices where the complaint is found."""
        raise NotImplementedError("This needs to be overwritten.")

    def check(
        self: "Complainer", text: OriginalTxt, converter: List[OriginalIdx]
    ) -> List[Complaint]:
        """Checks a piece of text and returns a complaint."""
        formatted_slices = self.find(text)
        out: List[Complaint] = []
        for sl in formatted_slices:
            original_slice = (converter[sl[0]], converter[sl[1]])
            out.append(Complainer._complain(sl=original_slice, text=text))
        return out
