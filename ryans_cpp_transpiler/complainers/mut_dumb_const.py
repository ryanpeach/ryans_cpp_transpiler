from typing import List, Dict

from py_idiomatic_regex import Regex

from ryans_cpp_transpiler.regex import NAME
from ryans_cpp_transpiler.complainers import Complainer

                
class MutDumbConstComplainer(Complainer):
    def find(self, text: str) -> List[slice]:
        """
        Using a mutable dumb pointer and a constant type is rediculous, because you could
        change the pointer and the value at deref would change. Don't do it.
        """
        # TODO: Make a lot more generic
        found: List[str] = Regex().literal("mut") \
                                             .whitespace() \
                                             .literal("dumb") \
                                             .whitespace() \
                                             .literal("const") \
                                             .whitespace() \
                                             .literal(NAME.n_or_more_repititions(2)) \
                                             .whitespace() \
                                             .literal('=') \
                                             .whitespace() \
                                             .anything() \
                                             .literal(';') \
                                             .find_all(text)

        return found