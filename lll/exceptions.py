from typing import (
    List,
    Optional,
)


class FormattedError(Exception):
    msg: str
    source_lines: List[str]
    line_offset: int
    col_offset: int
    mark_size: int
    file_name: Optional[str]

    def __init__(self,
                 msg: str,
                 source_code: str,
                 line_offset: int,
                 col_offset: int,
                 mark_size: int = 1,
                 file_name: str = None):
        self.msg = msg
        self.source_lines = source_code.splitlines()

        # Manually resolve negative offsets for error messages
        if line_offset < 0:
            self.line_offset = len(self.source_lines) + line_offset
        else:
            self.line_offset = line_offset
        if col_offset < 0:
            self.col_offset = len(self.source_lines[line_offset]) + col_offset
        else:
            self.col_offset = col_offset

        self.mark_size = mark_size
        self.file_name = file_name

    def __str__(self) -> str:
        if self.file_name is not None:
            prefix = self.file_name + ':'
        else:
            prefix = 'line '

        line_no = self.line_offset + 1
        col_no = self.col_offset + 1

        line = self.source_lines[self.line_offset]

        # Error mark reaches back from column offset
        mark = ' ' * (self.col_offset - self.mark_size + 1)
        mark += '^' * self.mark_size

        return f'{prefix}{line_no}:{col_no}: {self.msg}\n{line}\n{mark}'


class ParseError(FormattedError):
    pass
