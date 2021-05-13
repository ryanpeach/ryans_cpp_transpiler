import pytest

from ryans_cpp_transpiler.complainers import MutConstNotDeclared
from ryans_cpp_transpiler.utils.types import OriginalSlice, OriginalTxt


@pytest.mark.parametrize("txt", ["int var;", "int var();", "int var = val;",])
def test_mut_const_missing_simple(txt: str):
    assert MutConstNotDeclared.context.compile().fullmatch(
        txt
    ), f"Context did not match {txt}"

    complaints = MutConstNotDeclared.check_rcpp(
        original_txt=OriginalTxt(txt), context_range=OriginalSlice((0, len(txt)))
    )
    if not complaints:
        raise Exception(
            f'Did not correctly identify that mut or const is missing for simple case "{txt}"'
        )


@pytest.mark.parametrize(
    "txt",
    [
        "mut vector<int> var;",
        "mut vector<int> var();",
        "mut vector<int> var = val;",
        "const vector<int> var;",
        "const vector<int> var();",
        "const vector<int> var = val;",
        "mut map<const int, double> var;",
        "mut map<const int, double> var();",
        "mut map<const int, double> var = val;",
        "const map<mut int, double> var;",
        "const map<mut int, double> var();",
        "const map<mut int, double> var = val;",
    ],
)
def test_mut_const_missing_complex(txt: str):
    assert MutConstNotDeclared.context.compile().fullmatch(
        txt
    ), f"Context did not match {txt}"

    complaints = MutConstNotDeclared.check_rcpp(
        original_txt=OriginalTxt(txt), context_range=OriginalSlice((0, len(txt)))
    )
    if not complaints:
        raise Exception(
            f'Did not correctly identify that mut or const is missing for complex case "{txt}"'
        )


@pytest.mark.parametrize(
    "txt",
    [
        "mut ref(int) var;",
        "mut ref(int) var();",
        "mut ref(int) var = val;",
        "const ref(int) var;",
        "const ref(int) var();",
        "const ref(int) var = val;",
        "mut ref(dumb(mut vector<mut int>)) var;",
        "mut ref(dumb(mut vector<mut int>)) var();",
        "mut ref(dumb(mut vector<mut int>)) var = val;",
        "const ref(dumb(mut vector<mut int>)) var;",
        "const ref(dumb(mut vector<mut int>)) var();",
        "const ref(dumb(mut vector<mut int>)) var = val;",
    ],
)
def test_mut_const_missing_custom(txt: str):
    assert MutConstNotDeclared.context.compile().fullmatch(
        txt
    ), f"Context did not match {txt}"

    complaints = MutConstNotDeclared.check_rcpp(
        original_txt=OriginalTxt(txt), context_range=OriginalSlice((0, len(txt)))
    )
    if not complaints:
        raise Exception(
            f'Did not correctly identify that mut or const is missing for custom case "{txt}"'
        )
