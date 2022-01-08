from typing import overload

@overload
def check_for_docstring(output_location: None) -> None:
    ...

@overload
def check_for_docstring(output_location: str) -> None:
    ...
