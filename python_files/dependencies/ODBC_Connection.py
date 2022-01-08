"""
ODBC_Connection_functions.py

Connects to, and searches a given database.

*** Basic Connection String ****
connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=10.56.211.116\\sqlexpress;'
        'DATABASE=GetTheLeadOut;'
        'UID=' + input('Enter Username: ') + ';'
        'PWD=' + input('Enter Password: ') + ';'
        'charset=utf8;'

"""

# imports
import sys
from time import sleep

import requests

from os import getcwd
from os.path import dirname, abspath, join, isfile

import pyodbc

try:
    import python_files.dependencies.CustomLog_Classes as Clog
except ModuleNotFoundError:
    import dependencies.CustomLog_Classes as Clog

import tkinter.messagebox as msgbox


# noinspection PyAttributeOutsideInit
class DatabaseBasics:
    """ Allows for connecting to and basic querying of a SQL Database."""

    # All of the vars have a default value consistent with the GetTheLeadOut db.
    # Except uid and pw which are taken in by the GUI.
    def __init__(self, uid, pw, driver=None,
                 # '../Misc_Project_Files/msodbcsql17.dll',  # '{ODBC Driver 17 for SQL Server}',
                 server='10.56.211.116\\sqlexpress',
                 database='GetTheLeadOut',
                 charset='utf8'):

        # init error logging
        self.err = Clog.Error()
        self.err.error_setup()
        self.driver = driver
        self.driver_check(self.driver)

        # self.driver = driver

        self.server = server
        self.database = database

        # User must be non-domain at this point ie Andrew NOT amcsparron
        # uid and pw come from a variable passed into init by GUI_Class
        self.uid = uid  # input('Enter Username: ')
        self.pw = pw  # input('Enter Password: ')
        self.charset = charset

    def msi_get(self):
        """ If the MSI to install the MSSQL 17 Driver doesn't exist, attempt to download it. """

        try:
            choice = input('driver not found, '
                           'would you like to download the MS ODBC Driver 17 for SQL Server? (y/n): ').lower()

            if choice == 'y':
                print('Attempting to download MSI file to Misc_Project_Files...')
                # if its an EXE run
                if not getcwd().endswith('python_files'):

                    # if the MSI does not already exist in the misc project files folder or the exe root
                    if not isfile('.\Lead_GUI_Database\Misc_Project_Files\msodbcsql.msi') and not isfile(
                            'msodbcsql.msi'):

                        # use requests.post to download it from microsoft's site
                        req = requests.post('https://go.microsoft.com/fwlink/?linkid=2156851')

                        # open a binary file and write the content of requests to it
                        with open(r'.\Lead_GUI_Database\Misc_Project_Files\msodbcsql.msi', 'wb') as b:
                            b.write(req.content)

                        # if the file was downloaded successfully
                        if isfile('r.\Lead_GUI_Database\Misc_Project_Files\msodbcsql.msi'):
                            print('msi exists')
                            # TODO add in run of the msi

                    # if the msi does already exist, run it
                    elif isfile('.\Lead_GUI_Database\Misc_Project_Files\msodbcsql.msi'):
                        print('msi already exists, see Misc_Project_files.')
                        # TODO: add in run of the msi

                if getcwd().endswith('python_files'):
                    raise FileNotFoundError('This is a code run, ODBC Driver 17 for SQL Server should be installed?')

            if choice == 'n':
                raise FileNotFoundError('No Driver could be found and download was declined')

        except FileNotFoundError as e:
            self.err.error_handle(e)

        except Exception as e:
            self.err.error_handle(e)

    def driver_check(self, driver):
        """ check for the ideal driver, and use it if present.
        If that driver isn't available then use the generic driver.
        If the generic driver is not available,
        then attempt to download and install the ODBC Driver 17 for SQL Server.  """

        # TODO: add in a choose your driver option
        try:
            if self.driver is None:
                # check if OBDC Driver 17 exists, if it doesn't, use SQL Server
                if 'ODBC Driver 17 for SQL Server' not in pyodbc.drivers():
                    self.driver = '{SQL Server}'
                    print(self.driver)
                # if ODBC Driver 17 does exist, then use that
                elif 'ODBC Driver 17 for SQL Server' in pyodbc.drivers():
                    self.driver = '{ODBC Driver 17 for SQL Server}'
                    print(self.driver)
                else:
                    self.msi_get()

            elif self.driver is not None:
                # if they specify a driver, and its installed then use it
                if self.driver in pyodbc.drivers():
                    print('supplied driver found')
                    self.driver = driver

                # if they specify a driver and it IS NOT installed then raise an error
                elif self.driver not in pyodbc.drivers():
                    # TODO: add an "install driver" option
                    raise AttributeError('driver {name} was not found'.format(name=driver))
            else:
                raise AttributeError('Some other error occurred while detecting drivers')

        except AttributeError as e:
            self.err.error_handle(e)
        except pyodbc.Error as e:
            self.err.error_handle(e)

    def connect(self, con_type='non_azure'.lower()):
        """ Connect to a given database. """
        non_azure_connection_str = ('DRIVER={driver};'
                                    'SERVER={server};'
                                    'DATABASE={database};'
                                    'UID={uid};'
                                    'PWD={pwd};'
                                    'CHARSET={charset}'.format(driver=self.driver, server=self.server,
                                                               database=self.database,
                                                               uid=self.uid, pwd=self.pw, charset=self.charset))
        azure_connection_str = ('DRIVER={driver};'
                                'SERVER={server};'
                                'DATABASE={database};'
                                'CHARSET={charset};'
                                'Trusted_Connection=yes'.format(driver=self.driver, server=self.server,
                                                                database=self.database,
                                                                uid=self.uid, pwd=self.pw, charset=self.charset))
        # print(self.driver)
        errbox = ('Incorrect Credentials', 'Error:'
                                           '\nCould not log in'
                                           '\n Please check your username and password then try again')
        try:
            if con_type == 'non_azure':
                # try to connect to the db and pass the connection to the cnxn variable.
                cnxn = pyodbc.connect(non_azure_connection_str, timeout=5)

                # if the connection is made successfully
                if pyodbc.Connection:
                    print('Connection Successful')

                    # set the decoding and encoding to utf-8
                    cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
                    cnxn.setencoding(encoding='utf-8')

                    # return the connection to the db
                    return cnxn

            elif con_type == 'azure':
                # try to connect to the db and pass the connection to the cnxn variable.
                cnxn = pyodbc.connect(azure_connection_str, timeout=5)

                # if the connection is made successfully
                if pyodbc.Connection:
                    print('Connection Successful')

                    # set the decoding and encoding to utf-8
                    cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
                    cnxn.setencoding(encoding='utf-8')

                    # return the connection to the db
                    return cnxn
            else:
                raise AttributeError(
                    "con_type not valid, valid options are: 'azure' and 'non_azure'.\nPlease Try Again")

        except pyodbc.InterfaceError as e:
            # this doesnt exit on err so pw can be reattempted
            msgbox.showerror(errbox[0], errbox[1])
            self.err.error_handle_no_exit_quiet(e)

        except pyodbc.OperationalError as e:
            # this doesnt exit on err so pw can be reattempted
            self.err.error_handle_no_exit_quiet(e)
            msgbox.showerror(errbox[0], errbox[1])

        except AttributeError as e:
            self.err.error_handle_no_exit_quiet(e)
            msgbox.showerror(errbox[0], errbox[1])

        except Exception as e:
            # this doesnt exit on err so pw can be reattempted
            self.err.error_handle_no_exit_quiet(e)
            msgbox.showerror(errbox[0], errbox[1])

    def search(self, connection, table_name, column=None,
               col_val=None, operator=None, output_fields=None, should_print=bool(True), print_columns=bool(False)):
        """ Query a database based on:
        table_name, column, col_val, operator, output_fields

        choose whether or not results should be printed and or if the column names should be printed. """

        # if no output fields are specified, default to all fields
        if output_fields is None:
            output_fields = '*'

        self.should_print = should_print
        self.table_name = table_name
        self.cursor = connection.cursor()
        self.column = column  # limit to list of queryable params
        self.col_val = col_val  # limit to list of queryable params
        self.output_fields = output_fields  # limit to list of fields
        self.operator = operator  # =, <, >, <>(means not equal to)  etc
        self.print_columns = print_columns

        def print_columns():
            """ Print the columns of the given table. """
            other_cursor = connection.cursor()

            # gets a list of all the columns in the table
            other_cursor.execute(
                """ SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}' """.format(
                    table=self.table_name))
            self.columns = other_cursor.fetchall()
            self.valid_columns = []

            # for each of the columns returned by other_cursor.execute()
            for col in self.columns:
                # append the column name to self.valid_columns
                self.valid_columns.append(col[3])
            # delete the cursor used to get the column names
            del other_cursor

            print("\nValid columns are: \n")
            sleep(1)
            for vcol in self.valid_columns:
                print(vcol)

        if self.print_columns:
            print_columns()
            exit()

        elif not self.print_columns:
            try:
                if self.output_fields is not None and self.column is None and self.col_val is None:
                    print('****** Search Query below ******:\n')
                    print('Query is: ')
                    print(
                        """SELECT {out_fields} FROM {table}""".format(out_fields=self.output_fields, table=table_name))

                    self.cursor.execute(
                        """SELECT {out_fields} FROM {table}""".format(out_fields=self.output_fields, table=table_name))

                elif self.column is not None and self.col_val is not None and self.operator is not None:
                    print('****** Search Query below ******:\n')
                    print('Query is: ')
                    print(
                        """SELECT {out_fields} FROM {table} WHERE {col} {op} {col_val}""".format(
                            out_fields=self.output_fields,
                            table=table_name,
                            col=self.column,
                            op=self.operator,
                            col_val=self.col_val))
                    self.cursor.execute(
                        """SELECT {out_fields} FROM {table} WHERE {col} {op} {col_val}""".format(
                            out_fields=self.output_fields,
                            table=table_name,
                            col=self.column,
                            op=self.operator,
                            col_val='\'' +
                                    self.col_val + '\''))
                elif self.column is not None and self.col_val is None and self.operator is None:
                    raise AttributeError("If a column is selected then a value and operator must also be selected")

            except AttributeError as e:
                self.err.error_handle(e)

        rows = self.cursor.fetchall()

        if self.should_print:
            for row in rows:
                if len(row) > 1:
                    print(row)
                elif len(row) == 1:
                    print(row[0])

        elif not self.should_print:
            print("results not printed, but {rowlen} rows returned".format(rowlen=len(rows)))
            return rows

    def adv_query(self, connection, query):
        """ Queries the database based on a raw SQL statement. """
        output_list = []
        self.cursor = connection.cursor()

        try:
            self.cursor.execute('{query}'.format(query=query))

        except pyodbc.ProgrammingError as e:
            msgbox.showerror(title='Error', message=(str(e) + '\nPlease Try Again'))
            self.err.error_handle_no_exit_quiet(e)

        try:
            self.rows = self.cursor.fetchall()

        except pyodbc.ProgrammingError as e:
            self.err.error_handle_no_exit_quiet(e)

        except UnicodeDecodeError as e:
            # these errors usually only show up in the Comments column
            self.err.error_handle_no_exit_quiet(e)
            pass

        for row in self.rows:
            # test query
            # SELECT LName, FName, StreetAddress FROM GETTHELEADOUT WHERE FName = 'Andrew'

            # append the rows to the output_list, list
            output_list.append(row)

        # return the list and the query to adv_query
        return output_list, query

    # TODO: test me
    def exec_sql_file(self, connection, filepath, filename, print_return=False):
        try:
            if isfile(join(filepath, filename)):
                print("Executing file {fname}...".format(fname=filename))
                cursor = connection.cursor()
                cursor.execute(open(join(filepath, filename)).read())

                print("file execution complete")
                result = cursor.fetchall()

                if print_return:
                    for row in result:
                        print(row)
                    return result

                elif not print_return:
                    print('results returned but not printed')
                    return result

            elif not isfile(join(filepath, filename)):
                print('File, {fname}, '
                      '\nnot found in directory {fpath}.'
                      '\nPlease try again.'.format(fname=filename, fpath=filepath))

        except FileNotFoundError as e:
            self.err.error_handle_no_exit_quiet(e)
        except pyodbc.Error as e:
            self.err.error_handle_no_exit_quiet(e)


def db_connect(uid=None, pw=None, con_type='non_azure', server='10.56.211.116\\sqlexpress', db='GetTheLeadOut_Two'):
    # if the con_type is azure but server and db are non azure,
    # change to azure server and gisprod db

    if con_type == 'azure' and (server == '10.56.211.116\\sqlexpress'
                                or (db == 'GetTheLeadOut_Two' or db == 'GetTheLeadOut')):
        while True:
            con_mismatch = input('Connection type is azure but server and/or db attributes are non_azure defaults.\n'
                                 'Would you like to connect to the azure database GISPROD Server? (y/n): ').lower()
            if con_mismatch == 'y':
                server = 'P-ArcGIS-VAGOV-01\\sqlexpress'
                db = 'GISPROD'
                break

            elif con_mismatch == 'n':
                print('could not connect, goodbye.')
                exit(1)

            else:
                print('Please choose y or n...')
    else:
        pass

    try:
        if (uid is None or pw is None) and con_type == 'non_azure':
            raise AttributeError("non_azure connections require user name and password")

        elif (uid is None or pw is None) and con_type == 'azure':
            print('azure OS Creds used, connection made')

        elif (uid is not None and pw is not None) and con_type == 'non_azure':
            print('non_azure connection made, uid and pw used')

        else:
            raise AttributeError("Some other error occurred while validating connection params.\n"
                                 "user: {user}, connection_type: {contype}, "
                                 "server: {srv}, database: {db}".format(user=uid,
                                                                        contype=con_type,
                                                                        srv=server,
                                                                        db=db))
    except pyodbc.Error as e:
        err = Clog.Error()
        err.error_handle(e)

    except AttributeError as e:
        err = Clog.Error()
        err.error_handle(e)

    # create an instance of DatabaseBasics()
    c_inst = DatabaseBasics(uid, pw, server=server, database=db)

    # connect to the db and return the connection as conn_to_db
    con_to_db = c_inst.connect(con_type)

    # return con_to_db and c_inst
    return con_to_db, c_inst


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', dirname(abspath(__file__)))
    return join(base_path, relative_path)
