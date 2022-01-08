from typing import overload


class DatabaseBasics:
    """ Basic database connection and search. """

    @overload
    def __init__(self, uid: None, pw: None, driver: None = None,
                 # '../Misc_Project_Files/msodbcsql17.dll',  # '{ODBC Driver 17 for SQL Server}',
                 server: str = '10.56.211.116\\sqlexpress',
                 database: str = 'GetTheLeadOut',
                 charset: str = 'utf8'):
        ...

    @overload
    def __init__(self, uid: str, pw: str, driver: str,
                 server: str,
                 database: str,
                 charset: str):
        ...


    def msi_get(self) -> None:
        ...

    @overload
    def driver_check(self, driver: None) -> None:
        ...

    @overload
    def driver_check(self, driver: str) -> None:
        ...


    def connect(self, con_type: str) -> object:
        ...

    @overload
    def search(self, connection: object, table_name: str, column: None = None,
               col_val: None = None, operator: None = None,
               output_fields: None = None, should_print: bool = bool(True),
               print_columns: bool = bool(False)) -> list:
        ...

    @overload
    def search(self, connection: object, table_name: str, column: str,
               col_val: str, operator: str,
               output_fields: str, should_print: bool = bool(True),
               print_columns: bool = bool(False)) -> list:
        ...

    @overload
    def search(self, connection, table_name,
               column=None, col_val=None, operator=None,
               output_fields=None, should_print=bool(True),
               print_columns=bool(False)) -> list:
        ...

    @overload
    def search(self, connection, table_name,
               column=None, col_val=None, operator=None,
               output_fields=None, should_print=bool(True),
               print_columns=bool(False)) -> None:
        ...


    def adv_query(self, connection: object, query: str) -> tuple[list, str]:
        ...

@overload
def db_connect(uid: None = None, pw: None = None,
               con_type: str = 'non_azure',
               server: str = '10.56.211.116\\sqlexpress',
               db: str = 'GetTheLeadOut_Two') -> tuple[object, object]:
    ...

@overload
def db_connect(uid: str, pw: str,
               con_type: str, server: str,
               db: str) -> tuple[object, object]:
    ...
