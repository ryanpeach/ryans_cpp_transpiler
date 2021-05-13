from typing import List, Tuple

from ryans_cpp_transpiler.utils.types import HasContext, PartialSlice, PartialTxt
from src.ryans_cpp_transpiler.utils.types import ConvertedPartialTxt


class Converter(HasContext):
    """
    A class used to convert to and from cpp by defining one atomic rule.
    """

    @staticmethod
    def from_cpp(txt: PartialTxt,) -> List[Tuple[PartialSlice, ConvertedPartialTxt]]:
        """
        Converts text from cpp/hpp to rcpp/rhpp with input text that has no newlines and is
        whitespace agnostic.
        """
        raise NotImplementedError("Needs to be overwritten.")

    @staticmethod
    def to_cpp(txt: PartialTxt,) -> List[Tuple[PartialSlice, ConvertedPartialTxt]]:
        """
        Converts text from rcpp/rhpp to cpp/hpp with input text that has no newlines and is
        whitespace agnostic.
        """
        raise NotImplementedError("Needs to be overwritten.")
