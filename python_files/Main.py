#! python3
"""
PiMailbox

Monitors AWDGISPlans for new mail. When new mail is received,
the pi activates a servo and raises the flag/lights an LED.
"""


# imports
from os import system
from os.path import isdir, isfile
from sys import modules, version_info
import time

try:
    import dependencies.CustomLog_Classes as Clog
except ImportError:
    try:
        import CustomLog_Classes as Clog
    except ImportError:
        try:
            raise ImportError("Could not find CustomLog_Classes.py to import.")
        except ImportError:
            print('Clog could not be imported, use manual logging...')
            pass

try:
    from dependencies.yes_no import yes_no_loop as yn
except ImportError:
    try:
        from yes_no import yes_no_loop as yn
    except ImportError:
        raise ImportError("yn could not be imported, rewrite this portion")


# globals
if 'dependencies.CustomLog_Classes' in modules:
    err = Clog.Error()
    err.error_setup()
elif 'CustomLog_Classes' in modules:
    err = Clog.Error()
    err.error_setup()

elif 'dependencies.CustomLog_Classes' not in modules:
    print("CustomLog_Classes not in modules!!")

doc_check_token_path = "../Misc_Project_Files/no_doc_check"

py_ver_float = float(str(version_info.major) + '.' + str(version_info.minor))


# functions
def main_func(dev=False):
    """ Main Program function. """
    if not dev:
        # get start time in seconds since epoch
        start_time = time.time()

        print("Placeholder text")

        # calc time since start_time
        calc_runtime(start_time)
    elif dev:
        if version_info.major == 3:
            print("checking for docstrings now...")
            from dev_tests import interrogate_check as int_check
            int_check.check_for_docstring(None)
        elif py_ver_float <= 2.7:
            print("Python {version} does not support interrogate, please use python 3. Goodbye".format(
                version=float(str(version_info.major) + '.' + str(version_info.minor))))

            exit(0)
        else:
            print(str(version_info.major) + '.' + str(version_info.minor))


def calc_runtime(starttime):
    """ Calculate and print run time."""
    end_time = time.time()
    run_time = round(end_time - starttime, 3)
    if run_time > 60:
        print('run time is {rt} minutes'.format(rt=round(run_time / 60, 3)))
    elif not run_time > 60:
        print('run time is {rt} seconds'.format(rt=run_time))


def get_docs():
    """ Builds sphinx documentation using setup.py. """
    try:
        if isfile("../setup.py"):
            system("python ../setup.py build_sphinx -q")
        elif isfile('./setup.py'):
            system("python ./setup.py build_sphinx -q")
        else:
            # this is only in a try except loop since py2.7 does not have a FileNotFoundError
            try:
                raise FileNotFoundError("setup.py could not be found in project root, goodbye.")
            except Exception as e:
                err.error_handle(e)

    except FileNotFoundError as e:
        try:
            err.error_handle(e)
        except Exception:
            print(e)


def doc_check():
    """ Asks the user if Sphinx documentation should be generated."""
    if not isfile(doc_check_token_path):
        if py_ver_float <= 2.9:
            print("Program Documentation could not be generated, please use python 3 or greater.")
        elif py_ver_float >= 3.0:
            if isdir('../Program_Documentation') or isdir('Program_Documentation'):
                print("Program Documentation already exists. "
                      "Open Program_Documentation\html\index.html in a web browser to view it. "
                      "Moving on!")
            else:
                if yn("Project Documentation not found, would you like it to be generated?"):
                    get_docs()
                else:
                    if yn("Project docs not generated, would you like to be asked about this again?"):
                        pass
                    else:
                        with open(doc_check_token_path, "w") as f:
                            pass

    elif isfile(doc_check_token_path):
        print("no_doc_check_token detected, "
              "to check for documentation please delete {}".format(doc_check_token_path))


if __name__ == '__main__':
    try:
        doc_check()
    except NotADirectoryError as e:
        try:
            print("doc check failed, continuing on")
            # noinspection PyUnboundLocalVariable
            err.error_handle_no_exit_quiet(e)
        except UnboundLocalError as e:
            print("doc check failed, continuing on")
    except Exception as e:
        try:
            print("doc check failed, continuing on")
            # noinspection PyUnboundLocalVariable
            err.error_handle_no_exit_quiet(e)
        except UnboundLocalError as e:
            print("an error occurred that caused logging to fail, continuing on")

    main_func(dev=False)
