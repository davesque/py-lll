from lll.exceptions import (
    FormattedError,
)


SOURCE_CODE = """
(seq

    (def 'test-const 0xxff)

)
"""[1:-1]


def test_formatted_error_mark_placement():
    assert str(FormattedError(
        'test error',
        SOURCE_CODE,
        0, 0,
        mark_size=1,
        file_name=None,
    )) == """
line 1:1: test error
(seq
^
"""[1:-1]

    assert str(FormattedError(
        'test error',
        SOURCE_CODE,
        -1, -1,
        mark_size=1,
        file_name=None,
    )) == """
line 5:1: test error
)
^
"""[1:-1]

    assert str(FormattedError(
        'test error',
        SOURCE_CODE,
        -3, -2,
        mark_size=5,
        file_name=None,
    )) == """
line 3:26: test error
    (def 'test-const 0xxff)
                     ^^^^^
"""[1:-1]

    assert str(FormattedError(
        'test error',
        SOURCE_CODE,
        2, 25,
        mark_size=5,
        file_name=None,
    )) == """
line 3:26: test error
    (def 'test-const 0xxff)
                     ^^^^^
"""[1:-1]


def test_formatted_error_file_name():
    assert str(FormattedError(
        'test error',
        SOURCE_CODE,
        2, 25,
        mark_size=5,
        file_name='test.lll',
    )) == """
test.lll:3:26: test error
    (def 'test-const 0xxff)
                     ^^^^^
"""[1:-1]
