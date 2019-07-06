import io
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    TextIO,
    Union,
)

from lll.exceptions import (
    ParseError,
)


SExprList = List[Union[int, str, Any]]


WORD_SEPARATORS = {' ', '\t', '\n'}


class ParseBuffer:
    """
    Used to iterate over source code to be parsed while tracking parsing
    position.
    """
    __slots__ = ('source_code', 'file_name', 'line_offset', 'col_offset')

    source_code: str
    file_name: Optional[str]
    line_offset: int
    col_offset: int

    def __init__(self,
                 str_or_buffer: Union[str, TextIO],
                 file_name: str = None):
        if isinstance(str_or_buffer, str):
            self.source_code = str_or_buffer
        elif isinstance(str_or_buffer, io.TextIOWrapper):
            self.source_code = str_or_buffer.read()
        else:
            raise ValueError('unsupported input type for buffer')

        self.file_name = file_name

        # Parsing position
        self.line_offset = 0
        self.col_offset = 0

    def _handle_char(self, char: str) -> None:
        if char == '\n':
            self.line_offset += 1
            self.col_offset = 0
        else:
            self.col_offset += 1

    def __iter__(self) -> Iterator[str]:
        for char in self.source_code:
            yield char
            self._handle_char(char)

    def raise_error(self,
                          msg: str,
                          line_offset: int = None,
                          col_offset: int = None,
                          mark_size: int = 1) -> None:
        raise ParseError(
            msg,
            self.source_code,
            self.line_offset if line_offset is None else line_offset,
            self.col_offset if col_offset is None else col_offset,
            mark_size=mark_size,
            file_name=self.file_name,
        )


class Symbol(str):
    """
    String subclass that represents a parsed symbol (unquoted string) in an
    s-expression. For example, in the following s-expression
    ::

      (foo "bar" 1)

    the character sequence `foo` is a symbol whereas the character sequence
    `"bar"` is a string literal.
    """
    def __repr__(self) -> str:
        return str(self)


PREFIX_TO_INT_BASE = {
    '0x': 16,
    '0o': 8,
    '0b': 2,
}
DIGIT_CHARS = set('0123456789')


def _parse_symbol_or_int(buf: ParseBuffer, word: str) -> Union[int, str]:
    base: Optional[int]
    if word[0] in DIGIT_CHARS:
        # Default integer base is 10
        base = PREFIX_TO_INT_BASE.get(word[:2], 10)
    else:
        base = None

    try:
        if base is not None:
            # Try to parse this word as an integer with the appropriate base
            return int(word, base)
    except ValueError:
        buf.raise_error(
            f'invalid literal for int with base {base}: {repr(word)}',
            col_offset=buf.col_offset - 1,
            mark_size=len(word),
        )

    # Assume the word is a symbol
    return Symbol(word)


def parse_s_exp(str_or_buffer: Union[str, TextIO]) -> SExprList:
    """
    Parse the s-expression contained in a string or text buffer.

    (Adapted from https://en.wikipedia.org/wiki/S-expression#Parsing)

    :param str_or_buffer: A string or buffer containing an s-expression.

    :returns: A python list representation of the parsed s-expression.
    """
    buf = ParseBuffer(str_or_buffer)

    result_stack: List[SExprList] = [[]]
    symbol_or_int = ''
    str_literal = ''

    in_comment = False
    in_str = False
    in_str_escape = False

    for char in buf:
        # Parsing a comment
        if in_comment:
            # Comments end at the end of a line
            if char == '\n':
                in_comment = False
            # Otherwise, ignore char in comment

        elif not in_str:
            # Begin parsing a comment
            if char == ';':
                in_comment = True

            # Begin parsing an s-expression
            elif char == '(':
                result_stack.append([])

            # End an s-expression and add to result
            elif char == ')':
                # End a symbol or int literal and add to result
                if symbol_or_int:
                    result_stack[-1].append(_parse_symbol_or_int(buf, symbol_or_int))
                    symbol_or_int = ''

                temp = result_stack.pop()
                result_stack[-1].append(temp)

            elif char in WORD_SEPARATORS:
                # End a symbol or int literal and add to result
                if symbol_or_int:
                    result_stack[-1].append(_parse_symbol_or_int(buf, symbol_or_int))
                    symbol_or_int = ''
                # Otherwise, ignore the whitespace char

            # Begin parsing a string literal
            elif char == '"':
                in_str = True

            else:
                symbol_or_int += char

        # Parsing a string literal
        elif in_str:
            # Parsing a string escape sequence
            if in_str_escape:
                if char == '"':
                    str_literal += '"'
                elif char == '\\':
                    str_literal += '\\'
                elif char == 'n':
                    str_literal += '\n'
                elif char == 't':
                    str_literal += '\t'
                else:
                    str_literal += '\\' + char
                in_str_escape = False

            # Begin escape sequence in string
            elif char == '\\':
                in_str_escape = True

            # End string literal and add to result
            elif char == '"':
                result_stack[-1].append(str_literal)
                str_literal = ''
                in_str = False

            else:
                str_literal += char

        else:
            raise Exception('Unreachable')

    if in_str:
        buf.raise_error(
            'reached EOF before termination of string literal',
            line_offset=-1,
            col_offset=-1,
        )
    elif symbol_or_int or len(result_stack) > 1:
        buf.raise_error(
            'reached EOF before termination of s-expression',
            line_offset=-1,
            col_offset=-1,
        )

    return result_stack[0]
