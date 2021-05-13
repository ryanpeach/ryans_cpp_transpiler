from typing import List

from ryans_cpp_transpiler.complainers.mut_const_not_declared import MutConstNotDeclared
from src.ryans_cpp_transpiler.complainers.complainer_interface import Complainer

ALL_COMPLAINERS: List[Complainer] = [MutConstNotDeclared]

__all__ = ["Complainer", "ALL_COMPLAINERS"]
