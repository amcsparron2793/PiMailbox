"""
get_file_metadata.pyi


Get file information like creation time.

Also contains a function that checks
if a file is older than a given time,
as compared to the current time.
"""
from typing import overload
import datetime

def get_full_filestats(full_filepath: str, print_stats: bool=False) -> dict:
    ...

@overload
def get_create_time(full_filepath: str, readable: bool=False) -> int:
    ...

@overload
def get_create_time(full_filepath: str, readable: bool=True) -> datetime.datetime:
    ...

def check_expiration(full_filepath: str, length_of_validity: int) -> bool:
    ...