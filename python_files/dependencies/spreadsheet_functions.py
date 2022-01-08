"""
spreadsheet_functions.py

Classes for creating and initializing xlsx files using openpyxl,
as well as csv files using built in csv module.
"""
import csv
import json
from os.path import isfile
import openpyxl

import CustomLog_Classes as Clog
from yes_no import yes_no_loop as yn


# noinspection PyAttributeOutsideInit
class CsvHelper:
    """ Similar to SpreadsheetHelper for CSV files. """
    def __init__(self, csv_file_path):
        self.err = Clog.Error()
        self.err.error_setup()

        self.csv_file_path = csv_file_path

    def ReadDictCSV(self):
        """Reads a CSV file into a DictReader object,
        prints the results as a json,
        and returns the object."""

        if isfile(self.csv_file_path):
            try:
                with open(self.csv_file_path) as f:
                    CsvReaderInst = csv.DictReader(f)
                    for x in CsvReaderInst:
                        print(json.dumps(x, indent=4))
                return CsvReaderInst
            except IOError as e:
                self.err.error_handle(e)

    def _WriteToCSV(self, file_obj):
        """ Creates the DictWriter object, and writes the header
         and the dict_to_write defined in self.WriteDictToCSV."""
        try:
            csvDictWriterInst = csv.DictWriter(file_obj, self.csv_column_names)
            csvDictWriterInst.writeheader()

            # checks whether or not the dictionary to be written
            # is a list of dict rows, or just a single dictionary
            # list uses writerowS dict uses writeroW
            if type(self.dict_to_write) == list:
                csvDictWriterInst.writerows(self.dict_to_write)
            elif type(self.dict_to_write) == dict:
                csvDictWriterInst.writerow(self.dict_to_write)
            else:
                raise TypeError("dict_to_write must either be a dictionary, "
                                "or a list of dictionaries, NOT {}".format(type(self.dict_to_write)))
        except TypeError as e:
            self.err.error_handle(e)
        except Exception as e:
            self.err.error_handle(e)

    def WriteDictToCSV(self, dict_to_write, csv_column_names: list):
        """ Writes the given dictionary to self.csv_file_path
        with the given csv_column names."""

        self.csv_column_names = csv_column_names
        self.dict_to_write = dict_to_write

        if isfile(self.csv_file_path):
            overwrite = yn("{} already exists, would you like to overwrite it?".format(self.csv_file_path))
            if overwrite:
                try:
                    with open(self.csv_file_path, "w") as f:
                        self._WriteToCSV(f)
                except TypeError as e:
                    self.err.error_handle(e)
                except AttributeError as e:
                    self.err.error_handle(e)
                except Exception as e:
                    self.err.error_handle(e)
            elif not overwrite:
                try:
                    raise FileExistsError("{} already exists and was not overwritten, "
                                          "please try again".format(self.csv_file_path))
                except FileExistsError as e:
                    self.err.error_handle(e)

        elif not isfile(self.csv_file_path):
            with open(self.csv_file_path, "w") as f:
                self._WriteToCSV(f)
        print("{} Written".format(self.csv_file_path))


class SpreadsheetHelper:
    """Main Create and loading methods for xlsx files. """

    def __init__(self):
        self.err = Clog.Error()
        self.err.error_setup()

        self.wb = None
        self.sheet = None
        self.wb_path = None

    def create_wb(self, wb_path):
        """Create a workbook and sheet, save the file, then return both objects. """
        self.wb_path = wb_path

        # create a new openpyxl Workbook instance assigned to wb,
        # get the active sheet assigned to sheet.
        # Save it and return the two objects
        if not isfile(self.wb_path):
            try:
                self.wb = openpyxl.Workbook()
                self.sheet = self.wb.active
                self.wb.save(self.wb_path)
                print("{} Created in {}".format(self.wb_path.split("/")[-1],
                                                '/'.join(self.wb_path.split("/")[:-1])))
                return self.wb, self.sheet
            except FileNotFoundError as e:
                print("Directory does not exist, please try again.")
                self.err.error_handle(e)

    def setup_wb_and_sheet(self, wb=None, sheet=None, wb_path=None):
        """ Attempts to open a pre-existing xlsx file and get the active sheet,
         OR create a new sheet at wb_path using create_wb(). """
        self.wb_path = wb_path
        self.sheet = sheet
        self.wb = wb
        try:
            # if a path was given, and the path is a file then load the workbook and first sheet, return those values.
            if self.wb_path and isfile(self.wb_path):
                self.wb = openpyxl.load_workbook(self.wb_path)
                self.sheet = self.wb.active
                return self.wb, self.sheet, self.wb_path

            # if a path was given and the path is not a file, run create_wb with the path.
            # then return the objects.
            # unless the given path is the draft metadata file or the real metadata file, in that case error out.
            elif self.wb_path and not isfile(self.wb_path):
                if yn("{file} does not exist, would you like to create it?".format(file=self.wb_path)):
                    self.wb, self.sheet = self.create_wb(self.wb_path)
                    return self.wb, self.sheet, self.wb_path
                else:
                    raise FileNotFoundError("Given xlsx file does not exist and was not created.")

            # if no path was given and a workbook and sheet instance were given, return those.
            elif not self.wb_path and self.wb and self.sheet:
                return self.wb, self.sheet, self.wb_path

            # otherwise error out
            else:
                raise AttributeError("Either: wb instance AND sheet instance must not be none."
                                     "\nOR\n "
                                     "wb_path must not be None.")
        except AttributeError as e:
            self.err.error_handle(e)

        except Exception as e:
            self.err.error_handle(e)
