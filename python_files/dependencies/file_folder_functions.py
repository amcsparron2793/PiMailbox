""" file_folder_functions.py """

# imports
import json
import os

from os.path import join, isdir

try:
    import dependencies.CustomLog_Classes as Clog
except ModuleNotFoundError as e:
    try:
        import CustomLog_Classes as Clog
    except Exception as e:
        print("Could not import Clog")

from termcolor import colored
import py7zr
import questionary


# noinspection PyAttributeOutsideInit
class FileFolderFunctions:
    def __init__(self):
        self.err = Clog.Error()
        self.err.error_setup()

    def WriteDictToJson(self, dict_to_write, chosen_filename,
                        destination_dir="..\Misc_Project_Files", add_timestamp=False):
        """Writes a given dictionary to a json file with or without timestamp."""
        if isdir(destination_dir):
            if chosen_filename.endswith(".json"):
                chosen_filename = chosen_filename.split(".")[0]
            else:
                pass

            try:
                if not add_timestamp:
                    with open(join(destination_dir, '{fname}.json').format(fname=chosen_filename), 'w') as f:
                        json.dump(dict_to_write, fp=f, indent=4)

                elif add_timestamp:
                    from time import strftime
                    ts = str(strftime('%m-%d-%y') + '_' + strftime('%H%M_%p'))

                    with open(join(destination_dir, '{fname}_{ts}.json').format(fname=chosen_filename, ts=ts),
                              'w') as f:
                        json.dump(dict_to_write, fp=f, indent=4)

                print(colored('{json_name} dumped, see {json_path}'.format(json_name=f.name.split('\\')[-1],
                                                                           json_path=f.name), 'green'))

            except json.JSONDecodeError as e:
                self.err.error_handle(e)
            except WindowsError as e:
                if e.winerror == 22:
                    print(colored("error with filename, "
                                  "defaulting to \'default_json_filename.json\' with timestamp", "red"))

                    from time import strftime
                    ts = str(strftime('%m-%d-%y') + '_' + strftime('%H%M_%p'))

                    with open(join(destination_dir, '{fname}_{ts}.json').format(fname="default_json_filename", ts=ts),
                              'w') as f:
                        json.dump(dict_to_write, fp=f, indent=4)

                print(colored('{json_name} dumped, see {json_path}'.format(json_name=f.name.split('\\')[-1],
                                                                           json_path=f.name), 'green'))

            """except IOError as e:
                self.err.error_handle(e)"""
        else:
            try:
                raise FileNotFoundError("{} does not exist, please try again.".format(destination_dir))
            except FileNotFoundError as e:
                self.err.error_handle(e)

    def unpack_7z_archive(self, archive_file, path_to_file):
        """ unpacks a given archive file. """
        self.archive_file = archive_file
        self.path_to_file = path_to_file

        default_unpack_path = join(path_to_file, archive_file.split('.7z')[0]).replace('\\', '/')

        while True:
            self.unpack_destination = questionary.path("Please Enter destination for the unpacked archive",
                                                       default=default_unpack_path,
                                                       only_directories=True).ask()
            self.dest_conf = questionary.confirm("{} is your chosen destination, "
                                                 "are you sure?".format(self.unpack_destination))
            if self.unpack_destination == default_unpack_path:
                if os.path.isabs(self.unpack_destination):
                    success = self._check_and_extract()
                else:
                    print("{} is a relative path, attempting to convert it to absolute".format(self.unpack_destination))
                    print(os.path.abspath(self.unpack_destination))
                    self.unpack_destination = os.path.abspath(self.unpack_destination)
                    success = self._check_and_extract()
                if success:
                    break
                else:
                    print("extraction not successful, please try again")

            elif self.unpack_destination != default_unpack_path:
                if os.path.isabs(self.unpack_destination):
                    success = self._check_and_extract()
                else:
                    print("{} is a relative path, attempting to convert it to absolute".format(self.unpack_destination))
                    print(os.path.abspath(self.unpack_destination))
                    self.unpack_destination = os.path.abspath(self.unpack_destination)
                    success = self._check_and_extract()
                if success:
                    break
                else:
                    print("extraction not successful, please try again")

    def _check_and_extract(self):
        """ checks for destination dir, creates it if need be,
        and confirms placement, then calls self._extract_all_now()."""
        if isdir(self.unpack_destination):
            self.dest_conf.ask()
            if self.dest_conf:
                success = self._extract_all_now()
                return success
            elif not self.dest_conf:
                pass
        elif not isdir(self.unpack_destination):
            create_dest = questionary.confirm("{} does not exist, would you like to create it?".format(
                self.unpack_destination)).ask()
            if create_dest:
                try:
                    os.mkdir(self.unpack_destination)
                except PermissionError as e:
                    print("you do not have permission to create a directory there, please try again")
                    self.err.error_handle_no_exit_quiet(e)
                    pass

                except Exception as e:
                    self.err.error_handle(e)

                print("{} created!".format(self.unpack_destination))
                self.dest_conf.ask()
                if self.dest_conf:
                    success = self._extract_all_now()
                    return success
                elif not self.dest_conf:
                    pass
            elif not create_dest:
                print("destination was not created...")
                pass

    def _extract_all_now(self):
        """Runs py7zr.SevenZipFile() and its associated try: except: statements,
        returns true unless there are errors."""
        try:
            with py7zr.SevenZipFile(join(self.path_to_file, self.archive_file), 'r') as archive:
                archive.extractall(path=self.unpack_destination)
        except py7zr.exceptions.ArchiveError as e:
            self.err.error_handle(e)
        except Exception as e:
            self.err.error_handle(e)
        print("archive extracted to {}".format(self.unpack_destination))
        return True
