"""
get_file_metadata.py


Get file information like creation time.

Also contains a function that checks
if a file is older than a given time,
as compared to the current time.
"""

from pathlib import Path
from time import time
from datetime import datetime


def get_full_filestats(full_filepath, print_stats=False):
    """Get and print the full file stats for a given file, returns a dict. """

    fs_tuple_for_dict = []
    filestat_dict = {}

    rawstat = Path(full_filepath).stat()

    dirty_list = [r for r in str(rawstat).split('(')[1:]]
    clean_list = [d.split(')')[0] for d in dirty_list]

    for x in clean_list[0].split(','):
        fs_tuple_for_dict.append((x.split('=')[0], x.split('=')[1]))
    if print_stats:
        for x in fs_tuple_for_dict:
            print("{valname}: "
                  "\n{val}\n".format(valname=x[0].strip(), val=x[1]))
            filestat_dict.update({x[0].strip(): x[1]})

    elif not print_stats:
        for x in fs_tuple_for_dict:
            filestat_dict.update({x[0].strip(): x[1]})

    return filestat_dict


def get_create_time(full_filepath, readable=False):
    """ Returns Create Time using pathlib.Path.stat(),
    either in a human readable format, or the raw seconds since epoch"""

    raw_create_time = Path(full_filepath).stat()[-1]

    if not readable:
        return raw_create_time

    elif readable:
        # this is an easy way to take a raw time and turn it into a human friendly format
        create_time = datetime.fromtimestamp(raw_create_time)
        return create_time


def check_expiration(full_filepath, length_of_validity):
    """ Checks if a given file is 'expired' based on a given length of validity (in seconds)
        - 3,600 seconds - 1 hr
        - 28,800 seconds - 8 hrs
        - 43,200 seconds - 12 hrs
        - 86,400 seconds - 24 hrs """

    raw_create_time = Path(full_filepath).stat()[-1]
    exp_time = (raw_create_time + length_of_validity) # 28800)

    if time() >= exp_time:
        print("{file} has expired.".format(file=full_filepath.split('/')[-1]))
        return True

    elif time() <= exp_time:
        print("{file} has NOT expired.".format(file=full_filepath.split('/')[-1]))
        return False
