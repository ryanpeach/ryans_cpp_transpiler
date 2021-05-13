from iregex import Regex
from iregex.consts import ALPHA, ALPHA_NUMERIC, END_OF_LINE, NEWLINE

#: Just a set of parentheses with anything in them
_PARENTHESES = Regex(r"\(.*\)")

#: Just a set of angle brackets with anything in them
_ANGLE_BRACKETS = Regex(r"<.*>")

#: A literal double colon
_DOUBLE_COLON = Regex(r"::")

#: A literal semicolon
_SEMICOLON = Regex(r";")

#: A literal equals sign
_EQUALS = Regex(r"=")

#: A valid name with underscores allowed
NAME = (
    Regex(r"[a-zA-Z_]")
    + Regex().any_char("_", ALPHA_NUMERIC).zero_or_more_repetitions()
)

#: A valid type name
TYPE_NAME = (
    NAME + (_ANGLE_BRACKETS | _PARENTHESES).optional() + _DOUBLE_COLON.optional()
).one_or_more_repetitions()

#: A valid variable name
VARIABLE_NAME = NAME

#: A valid rvalue
RVALUE = Regex().anything()

#: Comment
INLINE_COMMENT = Regex(r"//").anything() + (Regex(NEWLINE) | Regex(END_OF_LINE))

#: An extension of whitespace before and after with newlines in between
MULTILINE_WHITESPACE = (
    Regex().whitespace() + INLINE_COMMENT.optional() + Regex().newline()
).one_or_more_repetitions()

#: A variable declaration like so:
#: TYPE_NAME VARIABLE_NAME;
VARIABLE_DECLARATION1 = (
    (TYPE_NAME + MULTILINE_WHITESPACE).one_or_more_repetitions()
    + VARIABLE_NAME
    + MULTILINE_WHITESPACE
    + _SEMICOLON
)

#: A variable declaration like so:
#: TYPE_NAME VARIABLE_NAME(ARGS);
VARIABLE_DECLARATION2 = (
    (TYPE_NAME + MULTILINE_WHITESPACE).one_or_more_repetitions()
    + VARIABLE_NAME
    + MULTILINE_WHITESPACE
    + _PARENTHESES
    + MULTILINE_WHITESPACE
    + _SEMICOLON
)

#: A variable declaration like so:
#: TYPE_NAME VARIABLE_NAME = RVALUE;
VARIABLE_DECLARATION3 = (
    (TYPE_NAME + MULTILINE_WHITESPACE).one_or_more_repetitions()
    + VARIABLE_NAME
    + MULTILINE_WHITESPACE
    + _EQUALS
    + MULTILINE_WHITESPACE
    + RVALUE
    + MULTILINE_WHITESPACE
    + _SEMICOLON
)

#: All valid variable declarations
VARIABLE_DECLARATION = (
    (TYPE_NAME + MULTILINE_WHITESPACE).one_or_more_repetitions()
    + VARIABLE_NAME
    + MULTILINE_WHITESPACE
    + (
        _SEMICOLON
        | (_PARENTHESES + MULTILINE_WHITESPACE + _SEMICOLON)
        | (_EQUALS + MULTILINE_WHITESPACE + RVALUE + MULTILINE_WHITESPACE + _SEMICOLON)
    )
)
