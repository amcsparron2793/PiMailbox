#! python3
""" CustomLog_Classes

Error handling Class and methods. """

from platform import system as p_system
import sys
from sys import exit
from os import mkdir, getcwd
from time import strftime
from os.path import isfile, isdir, join
from pathlib import Path
import traceback

# globals
if "windows" in p_system().lower():
    env_type = "windows"
else:
    env_type = "linux"

# defines the root project folder using pathlib.Path
project_root = Path(__file__).parent.parent

if str(project_root).endswith('python_files'):
    project_root = Path(__file__).parent.parent.parent

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable sys.executable'.
    application_path = sys.executable
    project_root = application_path.split('\\Main.exe')[0]

print("Project Root detected as: " + str(project_root))

# defines the log_root relative to the project root
log_root = join(str(project_root), 'logs')


def folder_check():
    """ Checks for and sets up the logging folder structure. """

    def _log_subdir_check():
        """ Checks for subdirs within the log folder. """
        if isdir(log_root + '/err_logs') and isdir(log_root + '/queries'):
            pass

        elif isdir(log_root + '/err_logs') and not isdir(log_root + '/queries'):
            mkdir(log_root + '/queries')
            print('missing \'queries\' log folder created')

        elif isdir(log_root + '/queries') and not isdir(log_root + '/err_logs'):
            mkdir(log_root + '/err_logs')
            print('missing \'err_logs\' folder created')

        elif not isdir(log_root + '/err_logs') and not isdir(log_root + '/queries'):
            mkdir(log_root + '/err_logs')
            mkdir(log_root + '/queries')
            print('Error and query log folder created!')

        if not isdir(log_root + '/queries/adv_queries'):
            mkdir(log_root + '/queries/adv_queries')
            print('advanced queries log folder created')

        elif isdir(log_root + '/queries/adv_queries'):
            pass

        if isdir(log_root + '/geoprocessing_logs'):
            pass

        elif not isdir(log_root + '/geoprocessing_logs'):
            mkdir(log_root + '/geoprocessing_logs')
            print('\'logs/geoprocessing_logs\' folder created!')

        if not isdir(log_root + '/other_logs'):
            mkdir(log_root + '/other_logs')

    # log folder check
    if not isdir(log_root):
        mkdir(log_root)
        print('log folder created!')

        _log_subdir_check()

    elif isdir(log_root):
        _log_subdir_check()

    # misc folder check
    if not isdir(join(str(project_root), 'Misc_Project_Files')):
        mkdir(join(str(project_root), 'Misc_Project_Files'))
        print('Misc_Project_Files folder created!')


class StdLog:
    """ Allows for logging of functions without printing to the console """

    def __init__(self):
        """ Initialize StdLog, check for logging folder structure
        and define the log file path and header for the file. """

        folder_check()
        if "WINDOWS" in env_type:
            self.run_log_file = (log_root + '/other_logs/run_log_' + strftime('%m-%d-%y') + '.log').replace("/", "\\")
        else:
            self.run_log_file = (log_root + '/other_logs/run_log_' + strftime('%m-%d-%y') + '.log')
        self.run_header = 'Log of run on ' + strftime('%m-%d-%y') + ' at ' + strftime('%H:%M %p') + ':'

    def std_log_setup(self):
        """ Set up the logging file objects in either write mode or append mode. """
        if isfile(self.run_log_file):
            self.fileobj = open(self.run_log_file, 'a')
        elif not isfile(self.run_log_file):
            self.fileobj = open(self.run_log_file, 'w')

    def std_log_write(self, function_to_log):
        """ write the given function to the fileobj. """
        self.function_to_log = function_to_log
        self.fileobj.write('\n' + self.run_header)
        self.fileobj.write('\n' + function_to_log)
        self.fileobj.write('\n******** END ***********\n')


# noinspection PyAttributeOutsideInit
class ArcpyLogging:
    """ Class for logging arcpy functions in /logs/geoprocessing_logs. """

    def __init__(self):
        """Initialize the class, check for folder structure, and define the log filepath.
        Then create the file objects in either write mode or append mode."""

        folder_check()
        if getcwd().endswith('python_files'):
            if "WINDOWS" in env_type:
                self.arc_log_file = (log_root + '/geoprocessing_logs/tool_log_'
                                     + strftime('%m-%d-%y') + '.log').replace("/", "\\")
            else:
                self.arc_log_file = (log_root + '/geoprocessing_logs/tool_log_'
                                     + strftime('%m-%d-%y') + '.log')
        elif not getcwd().endswith('python_files'):
            if "WINDOWS" in env_type:
                self.arc_log_file = (log_root + '/geoprocessing_logs/tool_log_'
                                     + strftime('%m-%d-%y') + '.log').replace("/", "\\")
            else:
                self.arc_log_file = (log_root + '/geoprocessing_logs/tool_log_'
                                     + strftime('%m-%d-%y') + '.log')

        if isfile(self.arc_log_file):
            self.arc_log_file_obj = open(self.arc_log_file, 'a')
        elif not isfile(self.arc_log_file):
            self.arc_log_file_obj = open(self.arc_log_file, 'w')

    @staticmethod
    def setup_arc_log_dir():
        """ Setup the arcgis specific logging directories.
        (This method is all but deprecated because of folder_check()'s ubiquity)"""
        print(getcwd())
        if isdir(log_root):
            if isdir(log_root + '/geoprocessing_logs'):
                print('\'logs/geoprocessing_logs\' folder detected')
            elif not isdir(log_root + '/geoprocessing_logs'):
                mkdir(log_root + '/geoprocessing_logs')
                print('\'logs/geoprocessing_logs\' folder created!')
        # TODO: Deprecated?
        elif not isdir(log_root) and isdir('./logs'):
            if isdir('./logs/geoprocessing_logs'):
                print('\'logs/geoprocessing_logs\' folder detected')
            elif not isdir('./logs/geoprocessing_logs'):
                mkdir('./logs/geoprocessing_logs')
                print('\'logs/geoprocessing_logs\' folder created!')

    def write_getmessage(self, msg):
        """ Write a message (usually arcpy.GetMessages()) to the GIS specific log. """
        self.arc_log_file_obj.write('\n\n' + str(msg))
        print('arcpy.GetMessages logged')


class Error:
    """ General Error Handling that is not tailored to any specific type of error. """

    def __init__(self):
        """ Initialize the Error class, check for log folders, and create a variable for the normal stderr.
        Create the error log filepath and the header for any error that is encountered., """

        folder_check()
        self.org_stderr = sys.stderr
        if getcwd().endswith('python_files'):
            if "WINDOWS" in env_type:
                self.err_file = (log_root + '/err_logs/error_log_' + strftime('%m-%d-%y') + '.log').replace("/", "\\")
            else:
                self.err_file = log_root + '/err_logs/error_log_' + strftime('%m-%d-%y') + '.log'
        elif not getcwd().endswith('python_files'):
            if "WINDOWS" in env_type:
                self.err_file = (log_root + '/err_logs/error_log_'
                                 + strftime('%m-%d-%y') + '.log').replace("/", "\\")
            else:
                self.err_file = log_root + '/err_logs/error_log_' + strftime('%m-%d-%y') + '.log'

        self.err_header = 'Error encountered on ' + strftime('%m-%d-%y') + ' at ' + strftime('%H:%M %p') + ':'

    def get_err_msg(self, exception):
        """ Get the exception that was encountered and format it. """
        try:
            msg = ('Error Occurred: \'{err}\', \nsee logs at '.format(err=
                                                                      [x for x in exception.args if x is not None][0])
                   + str(self.err_file))
            return msg
        except AttributeError as e:
            sys.stderr.write(str(e))
            return str(e)

    def error_handle(self, e):
        """ Get the error that was encountered using get_err_msg and write it to the log. Then Exit(1). """
        err_msg = self.get_err_msg(e)
        print(err_msg)
        self.error_write()
        exit(1)

    def error_handle_no_exit_quiet(self, e):
        """ Get the error that was encountered using get_err_msg and write it to the log, but don't exit afterward. """
        err_msg = self.get_err_msg(e)
        # print(err_msg)
        self.error_write()

    def error_setup(self):
        """ Setup the error log and redirect sys.stderr to the log. """
        if isfile(self.err_file):
            # if the log exists, append to it
            sys.stderr = open(self.err_file, 'a')

        elif not isfile(self.err_file):
            # since for some reason this file op errors out
            # when run in a non virtual env, I added a try, except clause
            try:
                # if the log doesn't exist, create it first
                sys.stderr = open(self.err_file, 'w')
            # TODO: Deprecated?
            except FileNotFoundError as e:
                self.err_file = './logs/err_logs/error_log_' + strftime('%m-%d-%y') + '.log'
                sys.stderr = open(self.err_file, 'w')
                self.error_handle_no_exit_quiet(e)

    def error_write(self):
        """ Write the error encountered to the log. """
        sys.stderr.write('\n' + self.err_header)
        for x in sys.exc_info():
            sys.stderr.write('\n' + str(x))
        sys.stderr.write('\n******** Full exc_info below ***********\n')
        traceback.print_tb(sys.exc_info()[2])
        sys.stderr.write('\n******** END ***********\n')
