import pprint

import pytest

from lll.parser import (
    parse_s_exp,
    ParseError,
)


def get_sexp_repr(obj):
    return pprint.pformat(obj, indent=1, width=80, depth=None, compact=False) + '\n'


def test_parseable_files_are_parseable(parseable_lll_file):
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


def test_parsing_ENS(get_parsed_fixture, get_fixture_contents):
    parsed = get_parsed_fixture('ENS.lll.lisp')
    parsed_repr = get_fixture_contents('ENS.lll.lisp.repr')

    assert get_sexp_repr(parsed) == parsed_repr
