# py-lll

[![Join the chat at https://gitter.im/ethereum/py-lll](https://badges.gitter.im/ethereum/py-lll.svg)](https://gitter.im/ethereum/py-lll?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://circleci.com/gh/ethereum/py-lll.svg?style=shield)](https://circleci.com/gh/ethereum/py-lll)
[![PyPI version](https://badge.fury.io/py/py-lll.svg)](https://badge.fury.io/py/py-lll)
[![Python versions](https://img.shields.io/pypi/pyversions/py-lll.svg)](https://pypi.python.org/pypi/py-lll)
[![Docs build](https://readthedocs.org/projects/py-lll/badge/?version=latest)](http://py-lll.readthedocs.io/en/latest/?badge=latest)
   

An LLL compiler for Python.

Read more in the [documentation on ReadTheDocs](https://py-lll.readthedocs.io/). [View the change log](https://py-lll.readthedocs.io/en/latest/releases.html).

## Quickstart

```sh
pip install py-lll
```

## Developer Setup

If you would like to hack on py-lll, please check out the [Snake Charmers
Tactical Manual](https://github.com/ethereum/snake-charmers-tactical-manual)
for information on how we do:

- Testing
- Pull Requests
- Code Style
- Documentation

### Development Environment Setup

You can set up your dev environment with:

```sh
git clone git@github.com:ethereum/py-lll.git
cd py-lll
virtualenv -p python3 venv
. venv/bin/activate
pip install -e .[dev]
```

### Testing Setup

During development, you might like to have tests run on every file save.

Show flake8 errors on file change:

```sh
# Test flake8
when-changed -v -s -r -1 lll/ tests/ -c "clear; flake8 lll tests && echo 'flake8 success' || echo 'error'"
```

Run multi-process tests in one command, but without color:

```sh
# in the project root:
pytest --numprocesses=4 --looponfail --maxfail=1
# the same thing, succinctly:
pytest -n 4 -f --maxfail=1
```

Run in one thread, with color and desktop notifications:

```sh
cd venv
ptw --onfail "notify-send -t 5000 'Test failure ⚠⚠⚠⚠⚠' 'python 3 test on py-lll failed'" ../tests ../lll
```

### Release setup

For Debian-like systems:
```
apt install pandoc
```

To release a new version:

```sh
make release bump=$$VERSION_PART_TO_BUMP$$
```

#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, specify which part to bump,
like `make release bump=minor` or `make release bump=devnum`. This is typically done from the
master branch, except when releasing a beta (in which case the beta is released from master,
and the previous stable branch is released from said branch). To include changes made with each
release, update "docs/releases.rst" with the changes, and apply commit directly to master 
before release.

If you are in a beta version, `make release bump=stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `make release bump="--new-version 4.0.0-alpha.1 devnum"`
