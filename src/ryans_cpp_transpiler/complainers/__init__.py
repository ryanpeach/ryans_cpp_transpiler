from typing import List

from src.ryans_cpp_transpiler.complainers.complainer_interface import (
    Complainer,
    Complaint,
)

ALL_COMPLAINERS: List[Complainer] = []

__all__ = ["Complaint", "Complainer"]
