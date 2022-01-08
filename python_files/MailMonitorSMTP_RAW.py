"""
***Email_Checker***

pseudo:
when i get an email at AWDGISPlans@albanyny.gov
Get the attached files - and save them to the project directory

based on code at https://medium.com/@sdoshi579/to-read-emails-and-download-attachments-in-python-6d7d6b60269

V 1.5 AJM - split into clean functions, added inline comments
V1.5 AJM 11/3/2020 - added log FOLDER check and create if need be
"""


import email
import imaplib
import os
import sys
import time
from socket import error
from sys import stderr

# make a var so that the stdout can be set back to its normal state
org_stdout = sys.stdout
# login try counter
t = 1

error_dir = '../logs_and_output/error_logs'
gen_log_dir = '../logs_and_output/gen_run_logs'


# noinspection PyBroadException
def mail_login(email_user):
    email_pass = input('Password: ')
    try:
        mail.login(email_user, email_pass)
    except ConnectionResetError:
        stderr.write(str(sys.exc_info()[1]))
        print(sys.exc_info()[1])


def setup_mail(e, savelocation):
    global mail
    global data
    global id_list

    # connect to outlook's imap server on port 993 and print its welcome screen
    try:
        """Server name: outlook.office365.com Port: 993 Encryption method: SSL"""
        mail = imaplib.IMAP4_SSL(host='outlook.office365.com', port=993)#("imap.gmail.com", 993)
        print(mail.welcome)
    except error:  # socket.error
        # FIXME: make this log to stderr fileoutput correctly - moving all logging to its own .py file might work best?
        #  Moving the logging to a new file should just be a matter of repointing stderr to logging.whateverfunction()
        #  and moving functions to a new .py file?
        print('Connection could not be made due to \'' + str(sys.exc_info()[1]) + '\', please try again later')
        sys.stderr.write(str(sys.exc_info()))
        e = True
        return e

    # set email, ask for password, login and select inbox
    email_user = 'amcsparron@albanyny.gov\\AWDGISPlans'  # raw_input('Email: ')
    print('Account: ' + email_user)
    # mail_login is my function
    mail_login(email_user)
    # these are two attributes of the imported mail module
    mail.list()
    mail.select(mailbox='inbox')

    # search for mail of any charset 'None' without any filter 'ALL' (ie To:, From: etc)
    # type just comes back as ok or not ok - ie if the request was successful
    # data is the numeric ID of each email found
    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    # mail_ids.split() - adds each mail id as an entry in id_list
    id_list = mail_ids.split()

    # print the date and time
    print(time.strftime('%x %X'))
    # TODO: if this is moved to logging_functions.py the check_email function would be called from logging_functions.py.
    #  this needs to be changed first before moving
    # if the email check log exists then append to it and run check_mail outputting to it
    if os.path.isfile(gen_log_dir + '/email_check_log_' + time.strftime('%m-%d-%y') + '.txt'):
        with open(gen_log_dir + '/email_check_log_' + time.strftime('%m-%d-%y') + '.txt', 'a+') as emailCheckLog:
            try:
                check_mail(emailCheckLog, data, savelocation)
            except ConnectionResetError:
                print('connection was reset, please try again later')
                emailCheckLog.write('Connection was reset, please try again later ' + str(sys.exc_info()[1]))

    # if the email check log and its parent folder
    # does not exist then create and write to it
    # and run check_mail outputting to it
    elif not os.path.isfile(gen_log_dir + '/email_check_log_' + time.strftime('%m-%d-%y') + '.txt') \
            and not os.path.isdir(gen_log_dir):
        os.makedirs(gen_log_dir)
        with open(gen_log_dir + '/email_check_log_' + time.strftime('%m-%d-%y') + '.txt', 'w+') as emailCheckLog:
            try:
                check_mail(emailCheckLog, data, savelocation)
            except ConnectionResetError:
                print('connection was reset, please try again later')
                emailCheckLog.write('Connection was reset, please try again later ' + str(sys.exc_info()[1]))

    # if the email check log does not exist
    # then create and write to it
    # and run check_mail outputting to it
    elif not os.path.isfile(gen_log_dir + '/email_check_log_' + time.strftime('%m-%d-%y') + '.txt'):
        with open(gen_log_dir + '/email_check_log_' + time.strftime('%m-%d-%y') + '.txt', 'w+') as emailCheckLog:
            try:
                check_mail(emailCheckLog, data, savelocation)
            except ConnectionResetError:
                print('connection was reset, please try again later')
                emailCheckLog.write('Connection was reset, please try again later ' + str(sys.exc_info()[1]))


def check_mail(email_check_log, data, savelocation):
    sys.stdout = email_check_log

    # this prints the date and time for the run.
    # it also splits up the runs and makes them more readable
    print('\n')
    print('***********')
    print(time.strftime('%x %X'))
    print('***********')
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]

        # converts byte literal to string removing b''
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # downloading attachments
        for part in email_message.walk():
            # this part comes from the snipped I don't understand yet...
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            # print(part.get_payload)

            fileName = part.get_filename()
            print(fileName)
            filePath = os.path.join(savelocation, fileName)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            print('Downloaded "{file}" from email titled "{subject}."'.format(file=fileName, subject=subject))

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
                print('From : ' + email_from + '\n')
                print('Subject : ' + email_subject + '\n')
                print(msg.get_payload(decode=True))
    cleanup_checkmail(email_check_log, savelocation)


def cleanup_checkmail(email_check_log, savelocation):
    # close the log
    email_check_log.close()
    # change stdout back to its default and print email check complete
    sys.stdout = org_stdout
    print('*****************')
    print('email check complete\n' + str(len(os.listdir(os.path.join(savelocation)))) + ' files to be sorted found')
    os.chdir('../')
    return savelocation

# this was previously run from Main.py - needs to be fixed up
def dl_or_not():
    """ asks whether or not to check for new messages in email (requires email_checkerV2_0.py)"""

    dl = input('Do you want to check for new reports?(y/n): ').lower()
    if dl == 'y':
        global savelocation
        # establish save location for found files
        # DONE: fix this so root dir is not needed

        # savelocation = os.path.join('../', input('Where should found files be saved? (must be in root subfolder): '))
        savelocation = os.path.join(G_root, 'Plans')
        print(savelocation)
        os.system('pause')

        # pass that established location to create_dl_folder
        create_dl_folder(savelocation)

        # change to the script dir and run email_checker
        os.chdir(script_dir)
        # if error occurs in setup_mail,
        # return n to dl_or_not() which allows program to move on
        if emcheck.setup_mail(e=False,
                              savelocation=savelocation):
            should_continue = input('error when attempting to check for new reports, '
                                    'would you like to continue? (y/n): ').lower()
            if should_continue == 'y':
                print('Continuing past new report check...')
                sys.stderr.write('Continuing past new report check...')
                savelocation = os.path.join(G_root, 'Plans')
                return 'n', savelocation
            elif should_continue == 'n':
                print('Ok, Quitting...')
                sys.exit()
            else:
                print('Please Choose Yes or No')
                dl_or_not()
        else:
            validoptions = []
            # this is my quick and dirty solution to savelocation
            # not being returned by dl_or_not if its declared by emcheck.setup_mail()
            script_files = ['.idea', 'python_files', 'venv']
            for x in os.listdir('./'):
                if x not in script_files:
                    validoptions.append(x)
            print(savelocation)
            savelocation = os.path.join(G_root, 'Plans')

            return savelocation
    elif dl == 'n':
        savelocation = os.path.join(G_root, 'Plans')
        if os.path.isdir(savelocation):
            pass
        elif not os.path.isdir(savelocation):
            create_dl_folder(savelocation)

        return 'n', savelocation
    else:
        print('please choose yes or no')
        dl_or_not()
