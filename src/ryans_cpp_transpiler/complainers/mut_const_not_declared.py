from typing import List

from ryans_cpp_transpiler.complainers.complainer_interface import Complainer
from ryans_cpp_transpiler.utils.regex import VARIABLE_DECLARATION
from ryans_cpp_transpiler.utils.types import (
    Complaint,
    OriginalSlice,
    OriginalTxt,
    PartialTxt,
)


class MutConstNotDeclared(Complainer):

    context = VARIABLE_DECLARATION

    @staticmethod
    def check_rcpp(
        original_txt: OriginalTxt, context_range: OriginalSlice
    ) -> List[Complaint]:
        """Checks a piece of text and returns a complaint."""
        partial_txt = PartialTxt(original_txt[context_range])
        raise NotImplementedError()
