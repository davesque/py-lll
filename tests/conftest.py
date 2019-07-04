from pathlib import (
    Path,
)

import pytest


FIXTURES_PATH = Path(__file__).parent / 'fixtures'
UNPARSEABLE_FIXTURES_PATH = FIXTURES_PATH / 'unparseable'

FIXTURES = list(sorted(FIXTURES_PATH.glob('*.lisp')))
UNPARSEABLE_FIXTURES = list(sorted(UNPARSEABLE_FIXTURES_PATH.glob('*.lisp')))


def get_id(path: Path) -> str:
    return str(path.resolve())


@pytest.fixture(
    params=FIXTURES,
    ids=map(get_id, FIXTURES),
)
def parseable_lll_file(request):
    return request.param


@pytest.fixture(
    params=UNPARSEABLE_FIXTURES,
    ids=map(get_id, UNPARSEABLE_FIXTURES),
)
def unparseable_lll_file(request):
    return request.param
