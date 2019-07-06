import pprint

import pytest

from lll.exceptions import (
    ParseError,
)
from lll.parser import (
    ParseBuffer,
    _parse_symbol_or_int,
    parse_s_exp,
)


def get_sexp_repr(obj):
    return pprint.pformat(obj, indent=1, width=80, depth=None, compact=False) + '\n'


def test_parse_buffer_yields_source_code_characters(get_fixture_contents):
    source_code = get_fixture_contents('string_literals.lll.lisp')

    buf = iter(ParseBuffer(source_code))

    res = []
    for char in buf:
        res.append(char)

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


@pytest.mark.parametrize(
    'input,expected',
    (
        ('0', 0),
        ('1', 1),
        ('255', 255),
        ('-0', 0),
        ('-1', -1),
        ('-255', -255),
        ('0x0', 0),
        ('0x1', 1),
        ('0xff', 255),
        ('-0x0', 0),
        ('-0x1', -1),
        ('-0xff', -255),
        ('0o0', 0),
        ('0o1', 1),
        ('0o377', 255),
        ('-0o0', 0),
        ('-0o1', -1),
        ('-0o377', -255),
        ('0b0', 0),
        ('0b1', 1),
        ('0b11111111', 255),
        ('-0b0', 0),
        ('-0b1', -1),
        ('-0b11111111', -255),
    ),
)
def test_parse_symbol_or_int_yields_ints(input, expected):
    assert _parse_symbol_or_int(None, input) == expected


@pytest.mark.parametrize(
    'input',
    (
        'foo',
        '-foo',
        '-',
        'x',
        '*',
        'seq',
        'camelCase',
        'dash-case',
    ),
)
def test_parse_symbol_or_int_yields_symbols(input):
    assert _parse_symbol_or_int(None, input) == input


@pytest.mark.parametrize(
    'input,match_exc_msg',
    (
        ('0aaa', "base 10: '0aaa'"),
        ('-0aaa', "base 10: '-0aaa'"),
        ('0xxf', "base 16: '0xxf'"),
        ('-0xxf', "base 16: '-0xxf'"),
        ('0oxf', "base 8: '0oxf'"),
        ('-0oxf', "base 8: '-0oxf'"),
        ('0bxf', "base 2: '0bxf'"),
        ('-0bxf', "base 2: '-0bxf'"),
    ),
)
def test_parse_symbol_or_int_raises_errors(input, match_exc_msg):
    buf = ParseBuffer(input)
    for char in buf:
        pass

    with pytest.raises(ParseError, match=match_exc_msg):
        assert _parse_symbol_or_int(buf, input) == match_exc_msg


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
