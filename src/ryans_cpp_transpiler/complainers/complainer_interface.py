from typing import List, Optional

from iregex import Regex

from ryans_cpp_transpiler.utils.types import (
    Complaint,
    HasContext,
    OriginalSlice,
    OriginalTxt,
)


class Complainer(HasContext):
    """Shows errors when it finds specific strings."""

    context: Optional[Regex]

    def check_rcpp(
        self, original_txt: OriginalTxt, context_range: OriginalSlice
    ) -> List[Complaint]:
        """Checks a piece of text and returns a complaint."""
        raise NotImplementedError("This needs to be overwritten.")
