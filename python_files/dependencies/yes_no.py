""" yes_no.py

Basic yes no loop.
"""

from sys import version_info

# globals
py_version = str(version_info.major) + '.' + str(version_info.minor)


def yes_no_loop(question):
    """Simple Yes No loop that returns True or False.
    If the version of python is 3.x then it uses input,
    otherwise it uses raw_input. """

    if float(py_version) <= 2.7:
        while True:
            # noinspection PyUnresolvedReferences
            q = raw_input(question + " (y/n) (press q to quit): ").lower()
            if q == 'y':
                return True

            elif q == 'n':
                return False

            elif q == 'q':
                exit(0)
            else:
                print('please choose \'y\', \'n\' or \'q\'')

    elif str(py_version).startswith('3'):
        while True:
            q = input(question + " (y/n) (press q to quit): ").lower()
            if q == 'y':
                return True

            elif q == 'n':
                return False

            elif q == 'q':
                exit(0)
            else:
                print('please choose \'y\', \'n\' or \'q\'')
