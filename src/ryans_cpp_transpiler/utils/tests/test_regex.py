import pytest

from ryans_cpp_transpiler.utils.regex import NAME, TYPE_NAME, VARIABLE_DECLARATION


@pytest.mark.parametrize(
    "txt", ["var", "_var", "var_", "var_name", "var_name_1", "v1R_"]
)
def test_name_good(txt: str) -> None:
    assert NAME.compile().fullmatch(txt), f"Match not found for {txt}"


@pytest.mark.parametrize("txt", ["1var", "1", "",])
def test_name_bad(txt: str) -> None:
    assert not NAME.compile().fullmatch(txt), f"Bad match found for {txt}"


@pytest.mark.parametrize("txt", [])
def test_type_name_good(txt: str) -> None:
    assert TYPE_NAME.compile().fullmatch(txt), f"Match not found for {txt}"


@pytest.mark.parametrize("txt", [])
def test_type_name_bad(txt: str) -> None:
    assert not TYPE_NAME.compile().fullmatch(txt), f"Bad match found for {txt}"


@pytest.mark.parametrize("txt", ["int var;", "int var();", "int var = val;",])
def test_variable_declaration_simple(txt: str):
    assert VARIABLE_DECLARATION.compile().fullmatch(txt), f"Match not found {txt}"


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
def test_variable_declaration_complex(txt: str):
    assert VARIABLE_DECLARATION.compile().fullmatch(txt), f"Match not found {txt}"


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
def test_variable_declaration_custom(txt: str):
    assert VARIABLE_DECLARATION.compile().fullmatch(txt), f"Match not found {txt}"
