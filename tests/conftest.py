import contextlib
from pathlib import (
    Path,
)

import pytest

from lll.parser import (
    parse_s_exp,
)


FIXTURES_PATH = Path(__file__).parent / 'fixtures'
UNPARSEABLE_FIXTURES_PATH = FIXTURES_PATH / 'unparseable'

FIXTURES = list(sorted(FIXTURES_PATH.glob('*.lisp')))
UNPARSEABLE_FIXTURES = list(sorted(UNPARSEABLE_FIXTURES_PATH.glob('*.lisp')))


def get_fixture_path_id(path: Path) -> str:
    return str(path.resolve())


@contextlib.contextmanager
def _open_fixture_file(filename, *args):
    fixture_path = FIXTURES_PATH / filename

    with open(fixture_path, *args) as f:
        yield f


@pytest.fixture(
    params=FIXTURES,
    ids=get_fixture_path_id,
)
def parseable_lll_file(request):
    return request.param


@pytest.fixture(
    params=UNPARSEABLE_FIXTURES,
    ids=get_fixture_path_id,
)
def unparseable_lll_file(request):
    return request.param


@pytest.fixture
def open_fixture_file():
    return _open_fixture_file


@pytest.fixture
def get_parsed_fixture():
    def _get_parsed_fixture(filename):
        with _open_fixture_file(filename, 'r') as f:
            return parse_s_exp(f)

    return _get_parsed_fixture
