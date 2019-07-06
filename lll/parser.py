import io
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    TextIO,
    Union,
)


SExprList = List[Union[int, str, Any]]


WORD_SEPARATORS = {' ', '\t', '\n'}


class ParseError(Exception):
    pass


class ParseBuffer:
    """
    Used to iterate over content to be parsed while tracking parsing position.
    """
    __slots__ = ('content', 'line_no', 'col_no')

    content: str
    line_no: int
    col_no: int

    def __init__(self, str_or_buffer: Union[str, TextIO]):
        if isinstance(str_or_buffer, str):
            self.content = str_or_buffer
        elif isinstance(str_or_buffer, io.TextIOWrapper):
            self.content = str_or_buffer.read()
        else:
            raise ValueError('Unsupported input type for buffer')

        # Parsing position
        self.line_no = 1
        self.col_no = 1

    def _handle_char(self, char: str) -> None:
        if char == '\n':
            self.line_no += 1
            self.col_no = 1
        else:
            self.col_no += 1

    def __iter__(self) -> Iterator[str]:
        for char in self.content:
            yield char
            self._handle_char(char)


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


def _parse_symbol_or_int(word: str) -> Union[int, str]:
    try:
        return int(word)
    except ValueError:
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
                    result_stack[-1].append(_parse_symbol_or_int(symbol_or_int))
                    symbol_or_int = ''

                temp = result_stack.pop()
                result_stack[-1].append(temp)

            elif char in WORD_SEPARATORS:
                # End a symbol or int literal and add to result
                if symbol_or_int:
                    result_stack[-1].append(_parse_symbol_or_int(symbol_or_int))
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
        raise ParseError('Reached EOF before termination of string literal')
    elif symbol_or_int or len(result_stack) > 1:
        raise ParseError('Reached EOF before termination of s-expression')

    return result_stack[0]
