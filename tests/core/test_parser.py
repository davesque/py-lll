import pytest

from lll.parser import (
    parse_s_exp,
    ParseError,
)


def test_parseable_files_yield_result(parseable_lll_file):
    with open(parseable_lll_file, 'r') as f:
        parse_s_exp(f)


def test_unparseable_files_raise_parse_error(unparseable_lll_file):
    with open(unparseable_lll_file, 'r') as f:
        with pytest.raises(ParseError):
            parse_s_exp(f)


def test_parsing_string_literals(get_parsed_fixture):
    parsed = get_parsed_fixture('string_literals.lll.lisp')

    assert parsed[0][1] == '1234'
    assert parsed[1][1] == 'test simple string'
    assert parsed[2][1] == 'test escaped quote " in string'
    assert parsed[3][1] == 'test escaped backslash \\ in string'
    assert parsed[4][1] == 'test escaped backslash \\n in string'
    assert parsed[5][1] == 'test newline\nin string'
    assert parsed[6][1] == 'test escaped newline \n in string'
    assert parsed[7][1] == 'test escaped tab \t in string'
