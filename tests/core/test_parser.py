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
