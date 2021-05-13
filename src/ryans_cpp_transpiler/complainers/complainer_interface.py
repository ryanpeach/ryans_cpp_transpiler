from typing import List

from ryans_cpp_transpiler.utils.types import (
    Complaint,
    HasContext,
    OriginalSlice,
    OriginalTxt,
)


class Complainer(HasContext):
    """Shows errors when it finds specific strings."""

    @staticmethod
    def check_rcpp(
        original_txt: OriginalTxt, context_range: OriginalSlice
    ) -> List[Complaint]:
        """Checks a piece of text and returns a complaint."""
        raise NotImplementedError("This needs to be overwritten.")
