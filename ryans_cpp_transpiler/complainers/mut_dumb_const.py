from typing import List

from py_idiomatic_regex import Regex

from ryans_cpp_transpiler.complainers import Complainer
from ryans_cpp_transpiler.utils.regex import NAME
from ryans_cpp_transpiler.utils.types import FormattedSlice2, FormattedTxt


class MutDumbConstComplainer(Complainer):
    """Tries to eliminate uses of mut dumb const type"""

    def find(self: "Complainer", text: FormattedTxt) -> List[FormattedSlice2]:
        """
        Using a mutable dumb pointer and a constant type is rediculous, because you could
        change the pointer and the value at deref would change. Don't do it.
        """
        # TODO: Make a lot more generic
        found: List[FormattedSlice2] = Regex().literal("mut").whitespace().literal(
            "dumb"
        ).whitespace().literal("const").whitespace().literal(
            NAME.n_or_more_repititions(2)
        ).whitespace().literal(
            "="
        ).whitespace().anything().literal(
            ";"
        ).find_all(
            text
        )

        return found
