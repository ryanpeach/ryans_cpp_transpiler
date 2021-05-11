from typing import List, Optional

from iregex import Regex

from ryans_cpp_transpiler.utils.types import (
    FormattedPartialSlice2,
    FormattedPartialTxt,
    FormattedSlice2,
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

    def find(self, text: FormattedPartialTxt) -> List[FormattedPartialSlice2]:
        """Returns a list of slices where the complaint is found."""
        raise NotImplementedError("This needs to be overwritten.")

    def check(
        self,
        original_text: OriginalTxt,
        context_range: FormattedSlice2,
        converter: List[OriginalIdx],
    ) -> List[Complaint]:
        """Checks a piece of text and returns a complaint."""
        start, _ = context_range
        formatted_slices = self.find(
            FormattedPartialTxt(original_text[context_range[0] : context_range[1]])
        )
        out: List[Complaint] = []
        for sl in formatted_slices:
            a, b = sl
            original_slice = (converter[a + start], converter[b + start])
            out.append(Complainer._complain(sl=original_slice, text=original_text))
        return out
