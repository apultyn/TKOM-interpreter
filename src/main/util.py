import sys
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


@contextmanager
def open_source(path: Optional[Path]):
    if path is not None:
        with path.open("r", encoding="utf-8", newline="") as file_handle:
            yield file_handle
    else:
        if sys.stdin.isatty():
            raise SystemExit("No source code supplied - use -i <file> or pipe data in.")
        yield sys.stdin
