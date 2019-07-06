import pprint

import pytest

from lll.exceptions import (
    ParseError,
)
from lll.parser import (
    ParseBuffer,
    parse_s_exp,
)


def get_sexp_repr(obj):
    return pprint.pformat(obj, indent=1, width=80, depth=None, compact=False) + '\n'


def test_parse_buffer_yields_source_code_characters(get_fixture_contents):
    source_code = get_fixture_contents('string_literals.lll.lisp')
    buf_it = iter(ParseBuffer(source_code))

    res = []
    while True:
        try:
            res.append(next(buf_it))
        except StopIteration:
            break

    assert ''.join(res) == source_code


def test_parse_buffer_tracks_offsets(get_fixture_contents):
    source_code = get_fixture_contents('string_literals.lll.lisp')

    buf = ParseBuffer(source_code)
    buf_it = iter(buf)

    res = []
    for _ in range(14):
        res.append(next(buf_it))

    assert ''.join(res) == '(foo "1234" 1)'
    assert buf.line_offset == 0
    assert buf.col_offset == 13

    res.append(next(buf_it))

    assert res[-1] == '\n'
    assert buf.line_offset == 0
    assert buf.col_offset == 14

    res.append(next(buf_it))

    assert res[-1] == '('
    assert buf.line_offset == 1
    assert buf.col_offset == 0

    while True:
        try:
            res.append(next(buf_it))
        except StopIteration:
            break

    assert ''.join(res) == source_code
    assert buf.line_offset == 9
    assert buf.col_offset == 0


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
