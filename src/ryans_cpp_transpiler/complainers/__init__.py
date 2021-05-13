from typing import List

from src.ryans_cpp_transpiler.complainers.complainer_interface import Complainer

ALL_COMPLAINERS: List[Complainer] = []

__all__ = ["Complainer"]
