from typing import List, Tuple

from ryans_cpp_transpiler.utils.types import (
    ConvertedPartialTxt,
    FormattedSlice2,
    FormattedTxt,
)


class Converter:
    """
    A class used to convert to and from cpp by defining one atomic rule.
    """

    @staticmethod
    def from_cpp(
        text: FormattedTxt,
    ) -> List[Tuple[FormattedSlice2, ConvertedPartialTxt]]:
        """
        Converts text from cpp/hpp to rcpp/rhpp with input text that has no newlines and is
        whitespace agnostic.
        """
        raise NotImplementedError("Needs to be overwritten.")

    @staticmethod
    def to_cpp(text: FormattedTxt) -> List[Tuple[FormattedSlice2, ConvertedPartialTxt]]:
        """
        Converts text from rcpp/rhpp to cpp/hpp with input text that has no newlines and is
        whitespace agnostic.
        """
        raise NotImplementedError("Needs to be overwritten.")