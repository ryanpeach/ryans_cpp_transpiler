from typing import List, Optional, Tuple

from iregex import Regex

from src.ryans_cpp_transpiler.utils.types import (
    ConvertedPartialTxt,
    FormattedPartialSlice2,
    FormattedPartialTxt,
)


class Converter:
    """
    A class used to convert to and from cpp by defining one atomic rule.
    """

    context: Optional[Regex]

    @staticmethod
    def from_cpp(
        text: FormattedPartialTxt,
    ) -> List[Tuple[FormattedPartialSlice2, ConvertedPartialTxt]]:
        """
        Converts text from cpp/hpp to rcpp/rhpp with input text that has no newlines and is
        whitespace agnostic.
        """
        raise NotImplementedError("Needs to be overwritten.")

    @staticmethod
    def to_cpp(
        text: FormattedPartialTxt,
    ) -> List[Tuple[FormattedPartialSlice2, ConvertedPartialTxt]]:
        """
        Converts text from rcpp/rhpp to cpp/hpp with input text that has no newlines and is
        whitespace agnostic.
        """
        raise NotImplementedError("Needs to be overwritten.")
