#! python3
"""
GetRemoteFiles.py

allows for connecting to, and downloading and uploading from/to FTP Servers.
allows for downloading files using Requests.Get from HTTP sites.

MyFTPTool.choose_ftp_func() should be used to make use of class
"""


# imports
import json
from os.path import isdir, join

import prompt_toolkit.output.win32
import questionary
from prompt_toolkit.output.win32 import NoConsoleScreenBufferError
import requests

import os
import ftplib

from sys import stderr, version_info
from socket import gaierror
try:
    import dependencies.CustomLog_Classes as Clog
    import dependencies.file_folder_functions as fff
except ModuleNotFoundError as e:
    import CustomLog_Classes as Clog
    import file_folder_functions as fff
# globals


# TODO: stub files
# Classes/Functions
class MyFTPTool:
    """ Connects to FTP for uploading and downloading."""
    def __init__(self):
        self.err = Clog.Error()
        self.err.error_setup()

        while True:
            try:
                self.hostname = self.getHostName()
                print("Attempting to connect to {}".format(self.hostname))
                self.FtpCxn = ftplib.FTP(host=self.hostname)
                break
            except gaierror as e:
                print("Host: {} could not be found. Please try again.".format(self.hostname))
                stderr.write("Host: {} could not be found. Please try again.".format(self.hostname))
                self.err.error_handle_no_exit_quiet(e)
            except WindowsError as e:
                if e.winerror == 10060 or e.winerror == 10061:
                    stderr.write("Host: {} could not be found. Please try again.\n".format(self.hostname))
                    self.err.error_handle_no_exit_quiet(e)
                else:
                    self.err.error_handle(e)

        print("**** Connection Successful! ****")
        self.login()

    # noinspection PyMethodMayBeStatic
    def getHostName(self):
        if version_info.major >= 3:
            hn = input("Please Enter HostName [192.168.1.98]: ")
        else:
            # noinspection PyUnresolvedReferences
            hn = raw_input("Please Enter HostName [192.168.1.98]: ")

        if len(hn) > 0:
            return hn
        else:
            hn = "192.168.1.98"
            return hn

    def login(self):
        while True:
            try:
                print("**** Please Login to {} ****".format(self.hostname))
                if self.FtpCxn.login(input("User: "), input("Password: ")):
                    print(self.FtpCxn.getwelcome())
                    print("****** Login Successful! ******")
                    break
                else:
                    stderr.write("Login not successful, please try again.")
                    #print("Login not successful, please try again.")
            except ftplib.error_perm as e:
                self.err.error_handle(e)

    def _get_ftp_dir(self):
        print("\nAvailable files/folders in {} are: ".format(" '{}' ".format(self.FtpCxn.pwd())))
        for item in self.FtpCxn.nlst():
            print(item)

        while True:
            new_ftp_dir = input("Choose a new folder (press q to quit): ")
            if new_ftp_dir in self.FtpCxn.nlst("-d"):
                self.FtpCxn.cwd(new_ftp_dir)
                print("Current FTP Server directory is: {}".format(self.FtpCxn.pwd()))
                break

            elif new_ftp_dir.lower() == 'q':
                print("Ok, Quitting...")
                exit(0)

            elif not os.path.isdir(new_ftp_dir):
                print("folder '{}' not found, please try again".format(new_ftp_dir))

    def _ftp_dir_list(self):
        print("\nAvailable files/folders in {} are: ".format(" '{}' ".format(self.FtpCxn.pwd())))
        for item in self.FtpCxn.nlst():
            print(item)

    def _get_save_dir(self):
        while True:
            try:
                choice = input("Please choose location of the file to upload"
                               "\n or the save location for the downloaded file (or type default) (press q to quit): ")
                if choice == 'q':
                    print("Ok, Quitting...")
                    exit(0)

                elif choice == 'default':
                    choice = '../Misc_Project_Files'
                    print("defaulting to {}".format(choice))
                    return choice

                elif os.path.isdir(choice):
                    print("Folder validated")
                    return choice

                elif not os.path.isdir(choice):
                    print("Folder not detected, please try again.")
            except FileNotFoundError as e:
                self.err.error_handle(e)

    def choose_file(self, transfer_type):
        self._ftp_dir_list()
        while True:
            change_dir_q = input("Would you like to change directories? (y/n or q to quit): ").lower()
            if change_dir_q == 'y':
                self._get_ftp_dir()
                break
            elif change_dir_q == 'n':
                break
            elif change_dir_q == 'q':
                print("Ok, Quitting...")
                exit(0)
            else:
                print("Please choose \'y\', \'n\', or press \'q\' to quit.")
        savedir = self._get_save_dir()
        try:
            os.chdir(savedir)
        except FileNotFoundError as e:
            self.err.error_handle(e)

        self._ftp_dir_list()
        while True:
            if transfer_type == 'upload':
                filename = input("Please enter the name of the file to upload: ")
                if filename in os.listdir(savedir):
                    print("{} chosen".format(filename))
                    return filename
                else:
                    print("\'{}\' not found in, \'{}\' please try again.".format(filename, savedir))

            elif transfer_type == 'download':
                filename = input("Please enter the name of the file to download: ")
                if filename in self.FtpCxn.nlst():
                    print("{} chosen".format(filename))
                    return filename
                else:
                    print("\'{}\' not found in, \'{}\' please try again.".format(filename, self.FtpCxn.pwd()))

    def attempt_download(self, filename):
        try:
            with open(filename, 'wb') as localfile:
                self.FtpCxn.retrbinary('RETR ' + filename, localfile.write, 1024)
                print('File downloaded successfully!')
        except ftplib.Error as e:
            self.err.error_handle_no_exit_quiet(e)
            stderr.write("\nError encountered: {}".format(e))
            os.remove(filename)

    def upload_file_to_ftp(self, filename):
        try:
            self.FtpCxn.storbinary('STOR ' + filename, open(filename, "rb"))
            print("{} uploaded".format(filename))
            self.choose_ftp_func()
        except ftplib.Error as e:
            print("Error, file could not be uploaded. \nErrormsg: {}".format(e))
            self.err.error_handle_no_exit_quiet(e)

    def choose_ftp_func(self):
        function_choices = {1: "Upload",
                            2: "Download",
                            3: "Change Directory"}

        for c in function_choices:
            print(str(c) + ". " + function_choices[c])

        # choose function loop
        while True:
            choice = input("Please Enter the line number of the function "
                           "you would like to run (or press q to quit): ").lower()
            if choice == 'q':
                print("Ok, Quitting...")
                exit(0)
            elif int(choice) in function_choices.keys():
                if function_choices[int(choice)].lower() == 'download':

                    file_to_download = self.choose_file(transfer_type='download')
                    self.attempt_download(file_to_download)
                elif function_choices[int(choice)].lower() == "upload":
                    file_to_download = self.choose_file(transfer_type='upload')
                    self.upload_file_to_ftp(file_to_download)
                break
            else:
                print("Please choose a line number from the list above.")


class GetFileHttp:
    """ Uses GET HTTP requests to download a given url. """
    def __init__(self, url, get_headers=False, save_headers=False,
                 get_content=True, headers_to_send=None, payload_to_send=None, req_type=None, auth=None):

        self.err = Clog.Error()
        self.err.error_setup()

        self.req_type = req_type
        if not self.req_type:
            self.req_type = self._GetReqType()
        else:
            if self.req_type.lower() == "get" or self.req_type.lower() == "post":
                pass
            else:
                try:
                    raise AttributeError("valid request types are \"get\" and \"post\" ")
                except AttributeError as e:
                    self.err.error_handle(e)

        self.headers_to_send = headers_to_send
        self.payload_to_send = payload_to_send
        self.get_headers = get_headers
        self.save_headers = save_headers
        self.get_content = get_content
        self.url = url
        self.auth = auth
        self.fff_inst = fff.FileFolderFunctions()
        self.r = None

        #self.MakeReq()
        #self.process_file()

    def MakeReq(self):
        try:
            if self.req_type.lower() == "post":
                self.r = requests.post(url=self.url, headers=self.headers_to_send,
                                       data=self.payload_to_send, auth=self.auth)
                return self.r
            if self.req_type == "get":
                self.r = requests.get(url=self.url, headers=self.headers_to_send,
                                      data=self.payload_to_send, auth=self.auth)
                return self.r
        except requests.exceptions.RequestException as e:
            self.err.error_handle(e)

    def _GetReqType(self):
        while True:
            try:
                req_type = questionary.select("Please choose http request type: ", ["get", "post"]).ask()
                if req_type is not None:
                    return req_type
                else:
                    pass
            except NoConsoleScreenBufferError as e:
                self.err.error_handle(e)
            except Exception as e:
                self.err.error_handle(e)

    def _get_content_type(self):
        if (self.r.headers['Content-Type'] == 'text/html'
                or 'text' in self.r.headers['Content-Type']
                or self.r.headers['Content-Type'] == 'html'):
            r_type = "text"
        elif (self.r.headers['Content-Type'] == 'application/octet-stream'
                or ('application' in self.r.headers['Content-Type'] and "json" not in self.r.headers['Content-Type'])):
            r_type = 'exe'

        elif "json" in self.r.headers['Content-Type']:
            r_type = 'json'

        else:
            print("Content Type detected as {}".format(self.r.headers["Content-Type"]))
            r_type = 'default'

        return r_type

    def process_response(self):
        if self.r:
            if self.get_headers:
                print(json.dumps(self.r.headers, indent=4))
            elif self.save_headers:
                self.fff_inst.WriteDictToJson(self.r.headers, "ReqHeaders", add_timestamp=True)
            elif self.save_headers and self.get_headers:
                print(json.dumps(self.r.headers, indent=4))
                self.fff_inst.WriteDictToJson(self.r.headers, "ReqHeaders", add_timestamp=True)

            if self.get_content:
                req_type = self._get_content_type()

                if req_type == "text":
                    if len(self.r.url.split('/')[-1]) > 0:
                        with open("../Misc_Project_Files/{}".format(self.r.url.split('/')[-1]), 'w') as f:
                            f.write(self.r.text)
                            print("{} written".format(self.r.url.split('.')[-1]))
                    else:
                        with open("../Misc_Project_Files/response.html", "w") as f:
                            f.write(self.r.text)
                            print("{} written".format(f.name.split('.')[-1]))

                elif req_type == "exe":
                    try:
                        with open("../Misc_Project_Files/{}".format(self.r.url.split('/')[-1]), 'wb') as f:
                            f.write(self.r.content)
                            print("{} written".format(self.r.url.split('.')[-1]))
                    except OSError as e:
                        try:
                            with open("../Misc_Project_Files/{}".format("default_filename"), 'wb') as f:
                                f.write(self.r.content)
                                print("{} written".format(self.r.url.split('.')[-1]))
                                self.err.error_handle_no_exit_quiet(e)
                        except Exception as e:
                            self.err.error_handle(e)

                elif req_type == "json":
                    try:
                        self.fff_inst.WriteDictToJson(self.r.json(), "{}".format(self.r.url.split('/')[-1]),
                                                      add_timestamp=True)
                    except Exception as e:
                        try:
                            self.fff_inst.WriteDictToJson(self.r.json(), "Default_Filename", add_timestamp=True)
                            self.err.error_handle_no_exit_quiet(e)
                        except Exception as e:
                            self.err.error_handle(e)

                else:
                    print("request type defaulted to text since req_type was not recognized.")
                    try:
                        with open("../Misc_Project_Files/{}".format(self.r.url.split('/')[-1]), 'w') as f:
                            f.write(self.r.text)
                            print("{} written".format(self.r.url.split('.')[-1]))
                    except IOError as e:
                        self.err.error_handle(e)
        elif not self.r.ok:
            try:
                stderr.write("Error: {},\n{}".format(self.r.status_code, self.r.reason))
                raise requests.exceptions.RequestException("Error: {},\n{}".format(self.r.status_code, self.r.reason))
            except requests.exceptions.RequestException as e:
                self.err.error_handle_no_exit_quiet(e)

    def LoadValueFromJson(self, file_to_load, dict_key):
        """Loads a specific value from a given json file based on the given dict_key."""
        if os.path.isfile(file_to_load):
            try:
                with open(file_to_load) as f:
                    loaded = json.loads(f.read())
                    if dict_key in loaded.keys():
                        print("{} found".format(dict_key))
                        return loaded[dict_key]
                    else:
                        raise KeyError("key could not be found in {}, please try again".format(file_to_load))
            except KeyError as e:
                self.err.error_handle(e)
        elif not os.path.isfile(file_to_load):
            try:
                raise FileNotFoundError(
                    "{} could not be found in {}".format(file_to_load, file_to_load.split("/")[:-1]))
            except FileNotFoundError as e:
                self.err.error_handle(e)

    def dl_7z_archive(self, url, save_location):
        """ downloads any 7zip url and saves it as an archive. """
        try:
            archive_filename = url.split('/')[-1]
            r = requests.get(url)
            if r.ok:
                if isdir(save_location):
                    with open(join(save_location, archive_filename), 'wb') as f:
                        f.write(r.content)
                    archive_name = f.name.split('\\')[-1]
                    return archive_name, save_location
        except Exception as e:
            self.err.error_handle(e)
