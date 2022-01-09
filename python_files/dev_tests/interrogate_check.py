"""interrogate_check.py

This module uses the interrogate module to check for docstring coverage in any given project.
It also outputs a report to /Misc_Project_Files/dev_notes/interrogate_need_docstring.txt
"""

from sys import stderr

try:
    import python_files.dependencies.CustomLog_Classes as Clog
except ImportError:
    import dependencies.CustomLog_Classes as Clog

try:
    from python_files.dependencies.yes_no import yes_no_loop as yn
except ImportError:
    from dependencies.yes_no import yes_no_loop as yn
    print("yn could not be imported")

from os import system
from os.path import join, isdir

try:
    from interrogate import coverage
except ImportError:
    imp = yn("interrogate.coverage could not be imported.\n Would you like to try to install it with pip?")
    if imp:
        try:
            system("pip install interrogate")
            from interrogate import coverage

        except ImportError as e:
            stderr.write("interrogate.coverage could not be imported, goodbye")
        except Exception as e:
            stderr.write(str(e))
    else:
        stderr.write("interrogate.coverage could not be imported. Goodbye")
        exit(1)

# globals
err = Clog.Error()


def check_for_docstring(output_location=None):
    """ Checks a python project for missing doc strings and outputs a report. """
    try:
        # when run from main, if run as standalone add an additional ../
        if isdir(join(Clog.log_root, 'other_logs')) or output_location is None:
            output_loc = join(Clog.log_root, 'other_logs', 'interrogate_need_docstring.txt')

        elif not isdir(join(Clog.log_root, 'other_logs')):
            if isdir(output_location):
                output_loc = output_location
            else:
                raise NotADirectoryError("{output_location} does not exist, and \'other_logs\' does not exist")
        else:
            raise NotADirectoryError("Both Default and given output location do not exist.")

        config = coverage.config.InterrogateConfig(ignore_init_method=True, ignore_init_module=True)
        cov = coverage.InterrogateCoverage(paths=['../python_files'], conf=config)

        results = cov.get_coverage()
        cov.print_results(results=results, verbosity=2, output=output_loc)
        print('Interrogate results logged to {output}'.format(output=output_loc))

    except TypeError as e:
        err.error_handle(e)
    except Exception as e:
        err.error_handle(e)
