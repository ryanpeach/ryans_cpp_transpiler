from typing import List

class Complainer:
    """Shows errors when it finds specific strings."""

    def __init__(self) -> None:
        pass

    def find(self, text: str) -> List[slice]:
        """Returns a list of slices where the complaint is found."""
        raise NotImplementedError("This needs to be overwritten.")

    def complain(self, sl: slice, whole_text: str) -> str:
        """Returns a string to printout describing the complaint."""
        raise NotImplementedError("This needs to be overwritten.")
