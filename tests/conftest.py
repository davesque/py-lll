from pathlib import (
    Path,
)

import pytest


FIXTURES_PATH = Path(__file__).parent / 'fixtures'
UNPARSEABLE_FIXTURES_PATH = FIXTURES_PATH / 'unparseable'

FIXTURES = list(sorted(FIXTURES_PATH.glob('*.lisp')))
UNPARSEABLE_FIXTURES = list(sorted(UNPARSEABLE_FIXTURES_PATH.glob('*.lisp')))


def get_fixture_path_id(path: Path) -> str:
    return str(path.resolve())


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
