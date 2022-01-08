from typing import overload, TextIO
from pathlib import Path


project_root:Path = Path(__file__).parent.parent
log_root:str

def folder_check() -> None:
    ...

def _log_subdir_check() -> None:
    ...

class StdLog:
    def __init__(self):
        # needed for random syntax warnings to go away
        self.run_log_file: str = None
        self.run_header: str = None
        self.fileobj: TextIO = None

    def std_log_setup(self) -> None:
        ...

    def std_log_write(self, function_to_log:object) -> None:
        ...

class ArcpyLogging:
    def __init__(self):
        self.arc_log_file: str = None
        self.arc_log_file_obj: TextIO  = None

    @staticmethod
    def setup_arc_log_dir() -> None:
        ...

    @overload
    def write_getmessage(self, msg: str) -> None:
        ...

    @overload
    def write_getmessage(self, msg: object) -> None:
        ...

class Error:
    def __init__(self):
        self.err_file: str = None
        self.err_header: str = None

    def get_err_message(self, exception:Exception) -> str:
        ...

    def error_handle(self, e:Exception):
        ...

    def error_handle_no_exit_quiet(self, e: Exception) -> None:
        ...

    def error_setup(self) -> None:
        ...

    def error_write(self) -> None:
        ...
