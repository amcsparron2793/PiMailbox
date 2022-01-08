from typing import overload
from pathlib import WindowsPath, PosixPath

class FileFolderFunctions:
    def __init__(self):
        ...

    @overload
    def WriteDictToJson(self, dict_to_write:dict, chosen_filename:str,
                        destination_dir:str="..\Misc_Project_Files", add_timestamp:bool=False):
        ...

    @overload
    def WriteDictToJson(self, dict_to_write:list[dict], chosen_filename:str,
                        destination_dir:str="..\Misc_Project_Files", add_timestamp:bool=False):
        ...

    @overload
    def unpack_7z_archive(self, archive_file:str, path_to_file:str):
        ...

    @overload
    def unpack_7z_archive(self, archive_file:str, path_to_file:WindowsPath) -> None:
        ...

    @overload
    def unpack_7z_archive(self, archive_file:str, path_to_file:PosixPath) -> None:
        ...

    def _check_and_extract(self) -> bool:
        ...

    def _extract_all_now(self) -> bool:
        ...